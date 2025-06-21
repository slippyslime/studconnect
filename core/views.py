from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages as django_messages
from django.db import transaction
from .forms import MessageForm, UserRegisterForm, ReplyForm
from .models import MessageStatus, Message


def switch_role(request, role):
    if role in ['student', 'teacher', 'dean']:
        request.session['active_role'] = role
    return redirect(reverse('home'))

def home(request):
    current_role = request.session.get('active_role', 'student')
    return render(request, 'core/home.html', {'current_role': current_role})

@login_required
def compose(request):
    active_role = request.session.get("active_role", request.user.role)

    if request.method == "POST":
        form = MessageForm(request.POST, user=request.user, active_role=active_role)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.save()
            form.save_m2m()

            MessageStatus.objects.bulk_create(
                [MessageStatus(message=msg, user=u) for u in msg.recipients.all()]
            )
            return redirect("inbox")
    else:
        form = MessageForm(user=request.user, active_role=active_role)

    return render(request, "core/compose.html", {"form": form})


@login_required
def inbox_view(request):
    current_user = request.user
    role = request.session.get("active_role", current_user.role)

    messages = Message.objects.filter(recipients=current_user).order_by("-created_at")

    return render(request, "core/inbox.html", {
        "messages": messages,
        "current_role": role,
    })

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            request.session['active_role'] = user.role
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, "core/register.html", {"form": form})

@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)

    if request.user != message.sender and request.user not in message.recipients.all():
        return redirect("inbox")

    if request.user != message.sender:
        status_obj, created = MessageStatus.objects.get_or_create(
            message=message,
            user=request.user,
            defaults={"status": MessageStatus.READ},
        )
        if not created and status_obj.status != MessageStatus.READ:
            status_obj.status = MessageStatus.READ
            status_obj.save()

    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            with transaction.atomic():

                reply = Message.objects.create(
                    sender=request.user,
                    subject=f"Re: {message.subject}" if message.subject else "",
                    body=form.cleaned_data["body"],
                )

                recipients = list(message.recipients.all())
                if message.sender != request.user:
                    recipients.append(message.sender)
                recipients = {u for u in recipients if u != request.user}
                reply.recipients.set(recipients)

                MessageStatus.objects.bulk_create(
                    [MessageStatus(message=reply, user=u) for u in recipients]
                )

                orig_status, _ = MessageStatus.objects.get_or_create(
                    message=message, user=request.user
                )
                orig_status.status = MessageStatus.REPLIED
                orig_status.save()

                django_messages.success(request, "Ответ отправлен.")
                return redirect("message_detail", pk=reply.pk)
    else:
        form = ReplyForm()

    statuses = []
    if request.user == message.sender:
        statuses = (
            MessageStatus.objects.filter(message=message)
            .select_related("user")
            .order_by("user__username")
        )

    return render(
        request,
        "core/message_detail.html",
        {
            "message": message,
            "form": form,
            "statuses": statuses,
        },
    )



@login_required
def outbox_view(request):
    messages_sent = Message.objects.filter(sender=request.user).order_by("-created_at")

    # annotate статус отправителя к каждому сообщению
    status_map = {
        s.message_id: s.status
        for s in MessageStatus.objects.filter(message__in=messages_sent, user=request.user)
    }

    for msg in messages_sent:
        if any(s.status == MessageStatus.REPLIED for s in msg.messagestatus_set.all()):
            msg.status_display = "Отвечено"
        elif any(s.status == MessageStatus.READ for s in msg.messagestatus_set.all()):
            msg.status_display = "Прочитано"
        else:
            msg.status_display = "Отправлено"

    return render(request, "core/outbox.html", {
        "messages": messages_sent,
    })