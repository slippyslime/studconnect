from django.contrib import admin
from django.urls import path
from core import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("switch-role/<str:role>/", views.switch_role, name="switch_role"),
    path("admin/", admin.site.urls),
    path("messages/compose/", views.compose, name="compose"),
    path("inbox/", views.inbox_view, name="inbox"),
    path("register/", views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path("messages/<int:pk>/", views.message_detail, name="message_detail"),
    path("outbox/", views.outbox_view, name="outbox"),
]