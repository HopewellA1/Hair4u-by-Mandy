
from django.urls import path
from LoginManager import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #path('', views.home, name="home"),
    path('Signup', views.signupuser, name="Signup"),
    path('login', views.loginuser, name="login"),
    path('logoutuser', views.logoutuser, name="logoutuser"),
    path('resert', views.resetPassword, name="reset"),
    #path('register_view', views.register_view, name="register"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    
    #Password reset
    path('reset_password', views.password_reset_request, name="reset_password"),
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name ="LoginManager/password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name ="LoginManager/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name ="LoginManager/password_reset_done.html"), name="password_reset_complete"),
    path('change_password', auth_views.PasswordChangeView.as_view(template_name="LoginManager/changepassword.html"), name="change_password"),
    path('password_change_done',auth_views.PasswordChangeDoneView.as_view(template_name="LoginManager/passwordChangeDone.html"), name="password_change_done"),
    path('account', views.account, name="account")



]