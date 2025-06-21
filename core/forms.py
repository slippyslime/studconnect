from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Message, User

class MessageForm(forms.ModelForm):
    recipients = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        label="Кому",
    )

    class Meta:
        model = Message
        fields = ("recipients", "subject", "body")
        widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
        }

    def __init__(self, *args, **kwargs):
        active_role = kwargs.pop("active_role")
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

        if active_role == User.STUDENT:
            qs = User.objects.filter(role__in=[User.TEACHER, User.DEAN])
        elif active_role == User.TEACHER:
            qs = User.objects.filter(role=User.STUDENT)
        else:  # DEAN
            qs = User.objects.exclude(id=user.id)

        self.fields["recipients"].queryset = qs.order_by("username")


class ReplyForm(forms.Form):
    body = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        label="Ответ",
    )


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.STUDENT
        if commit:
            user.save()
        return user
