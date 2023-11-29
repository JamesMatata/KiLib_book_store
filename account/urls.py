from django.urls import path, reverse_lazy
from django.views.generic import TemplateView

from . import views
from .views import register, loginn, logoutuser, dashboard, add_to_wishlist, wishlist, edit_details, delete_user
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('register/', register, name="register-page"),
    path('activate/<slug:uidb64>/<slug:token>', views.account_activate, name='activate'),
    path('login/', loginn, name="login-page"),
    path('logout/', logoutuser, name='logout'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='account/password_reset_form.html',
                                              email_template_name='account/password_reset_email.html',
                                              success_url=reverse_lazy('account:password_reset_done')),
         name="password_reset"),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html',
                                                     success_url=reverse_lazy('account:password_reset_complete')),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='account/dashboard/password_change_form.html',
                                               success_url=reverse_lazy('account:password_change_done')),
         name="password_change_view"),
    path('password_change_done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='account/dashboard/password_change_done.html'),
         name="password_change_done"),
    # Wishlist
    path("wishlist/", wishlist, name="wishlist"),
    path("wishlist/add_to_wishlist/<int:id>", add_to_wishlist, name="user_wishlist"),

    path('dashboard/', dashboard, name="dashboard"),
    path('profile/edit/', edit_details, name='edit_details'),
    path('profile/delete_user/', delete_user, name='delete_user'),
    path('profile/delete_confirm/', TemplateView.as_view(template_name="account/dashboard/delete_confirm.html"),
         name='delete_confirmation')
]
