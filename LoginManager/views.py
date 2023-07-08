#from asyncio.windows_events import NULL
import email
from email import message
from hashlib import new
from tracemalloc import DomainFilter
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from LoginManager.models import Account
from .forms import registrationform
#from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django import forms
from .tokens import account_activation_token, Password_Reset_token
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator



#User = get_user_model()
def ActivationEmail(request, user, to_email):
    mail_subject = "Acivate your account."
    message = render_to_string("LoginManager/ActivationTemplate.html",{
        'user':user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    print(to_email)
    if send_mail(mail_subject,f"{message}"  ,'admin@kznsc.com',[f'{to_email}'], fail_silently=False,
    ):
        return messages.success(request,f"Verification email sent to {to_email}, please verify to access your account.")
    else:
        return messages.error(request, f"There was an erroe sening verification email, please ensure you enter the correct email")        

def ResertEmail(request, user, to_email):
    print(f"To user: {user.username}")
    mail_subject = "Reset your password."
    message = render_to_string("LoginManager/resertTemplate.html",{
        'user':user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    print(to_email)
    if send_mail(mail_subject,f"{message}"  ,'admin@kznsc.com',[f'{to_email}'], fail_silently=False,
    ):
        return messages.success(request,f"Click on the link that has been sent to {to_email}, to reset your password.")
    else:
        return messages.error(request, f"There was an erroe sening verification email, please ensure you enter the correct email")        

    
        
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
        
    if user != None and account_activation_token.check_token(user, token):
        user.is_active = True
        messages.success(request,f"welcome {user.username}, your account has been verified and made active please proceed to login")
        user.save()
       
    return redirect('home')
          
def register_view(request, *args, **kwargs):
    
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f"You already authenticated as {user.email}.") 
    if request.method == 'GET':
        return render(request,'LoginManager/signup.html')
    else:
       
        email = request.POST['email'].lower()
    
        account =""
        try:
            account = Account.objects.get(email = email)
        except Exception as e:
            print(e)
            #raise forms.ValidationError(f"Email {email} already exists on the system.")

        if account:
               return render(request,'LoginManager/signup.html',{ 'error':f"Email {email} already exists on the system."})

       
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = Account.objects.create_user(email= request.POST['email'].lower(),username= request.POST['username'],password = request.POST['password1'],)# email = request.POST['email'],
                
                user.is_active = False
              #  user.save(commit=False)
                user.save()
                
                print(ActivationEmail(request, user, request.POST['email'].lower()))
               # login(request,user)
               
               
                return redirect('home')
            except IntegrityError:
                return render(request,'LoginManager/signup.html',{ 'error':'Username Already Taken'})
            
        else:
            return render(request,'LoginManager/signup.html',{ 'error':'Passwords did not match'})
        



def home(request):
    if request.user.is_authenticated == True:
        print(request.user)
        return render(request,'LoginManager/home.html')
        
    return render(request,'LoginManager/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request,'LoginManager/signup.html',{'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(first_name = request.POST["first_name"],last_name = request.POST["last_name"],username = request.POST['email'].lower(),email =request.POST['email'].lower(), password = request.POST['password1'],)# email = request.POST['email'],
                user.is_active = False
                user.save()
                ActivationEmail(request, user, request.POST['email'].lower())
                #login(request,user)
                messages.success(request,"Account created successfully, an email has been sent for activation please visit email ("+request.POST['email'].lower()+") to activate your account.")
                return redirect('home')
            except IntegrityError:
                messages.error(request, "something went wrong please try again.")
                return render(request,'LoginManager/signup.html',{'form':UserCreationForm(), 'error':'Username Already Taken'})
            
        else:
            return render(request,'LoginManager/signup.html',{'form':UserCreationForm(), 'error':'Passwords did not match'})
        
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    if request.method =='GET':
        logout(request)
        return redirect('home')
    
def loginuser(request):
    if request.method == 'GET':
        return render(request,'LoginManager/login.html',)
    else:
        try:
            user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
        except:
            messages.error(request,"Please check your connection, something went wrong.")
            
        if user is None:
            return render(request, 'LoginManager/login.html', {'form':AuthenticationForm(), 'error':'email and password did not match'})
        else:
            login(request,user) 
            if user.is_active == False:
                messages.error(request, f"Hello {user.username}, please login to your email and activate your account. Verification email sent to {user.email}") 
            return redirect('home')
# my recent activity is reserting the passord and maybe email      
def resetPassword(request, **kwargs):
        user = request.user
        #if we are coming from the email link
       
            
       # if user.is_authenticated == False:
            
            
        if request.method == 'GET':
           
            return render(request, 'LoginManager/resertPassword.html')
        else:

            if kwargs:
                if kwargs.uidb64:
                    User = get_user_model()              
                    try:
                        uid = force_str(urlsafe_base64_decode(kwargs.uidb64))
                        user = Account.objects.get(pk=uid)
                    except:
                            
                        return HttpResponse(f"Something went wrong while tring to retieve your acoount, try revisiting the link from the email.") 
                
        
                 
            if request.POST['password1'] == request.POST['password2']:
                try:
                    user = Account.objects.get(email = user.email) 
                        
                    
                    if request.POST['email'].lower():
                        user.email = request.POST['email'].lower()
                            
                    if request.POST['username']:
                        user.username = request.POST['username']
                    
                    #
                   
                        
                
                    user.password =  request.POST['password1']
                   
                            
                    #  user.save(commit=False)
                    user.save()
                    messages.success(request,f"{user.username} your account infomation has been updated successfully, you can proceed to login")
                    #print(ActivationEmail(request, user, request.POST['email'].lower()))
                    
                    # login(request,user)
                    
                    
                    return redirect('home')
                except IntegrityError:
                    return render(request,'LoginManager/signup.html',{ 'error':'Username Already Taken'})
            else:
                messages.error(request,f"New password does not match the confirmed password.")
                return render(request, 'LoginManager/resertPassword.html') 
                
                
def password_reset_request(request):
    #ResertEmail
   
    if request.method =='POST':
        password_form = PasswordResetForm(request.POST)
        if password_form.is_valid():
            user =None
            data = password_form.cleaned_data['email']
            try:
                user =get_object_or_404(User,username = data) 
            except:
                pass
          
           
            if user:
                ResertEmail(request,user,data)
                
                return redirect("home")
            else:
                messages.error(request, "we could not find your account please enter the email you used to create an account or contact the admin")
                return redirect("home")
                
            
                
            
 
                
    else:
        password_form = PasswordResetForm()
        context = {
        'password_form': password_form,
        }
    return render(request,'LoginManager/password_reset.html', context)  
            
            
#in the acctount function you can update 
@login_required
def account(request):
    user = request.user
    
    if request.method == 'GET':
        
        return render(request, 'LoginManager/account.html')
    
    if request.method == 'POST':
        numUpdates = 0
        if user.first_name != request.POST["first_name"]:
            user.first_name = request.POST["first_name"]
            numUpdates += 1
            
        if user.last_name != request.POST["last_name"]:
            user.last_name = request.POST["last_name"]
            numUpdates += 1
        
        if user.email != request.POST["email"]:
            user.email = request.POST["email"]
            numUpdates += 1
            
        if numUpdates > 0:
            messages.success(request, "Account changes made succesfully.")
            user.save()
        else:
            messages.warning(request, "No changes detected.")
            
        return redirect("account")
     
                
                
                
                
                
                
                
                
                
                
                
             
    
        
