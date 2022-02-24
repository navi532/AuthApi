

from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer,LoginSerializer,ResetSerializer,PasswordResetSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
import jwt
from django.core.mail import send_mail
from django.utils.encoding import force_bytes,force_text
from django.contrib.auth.models import User,update_last_login
from .tokens import account_token
from django.urls import reverse
from .models import Loginhistory,Extendeduser

# Create your views here.
class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self,request):
        serializer = UserSerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save()

            user = User.objects.get(email = serializer.data['email'])
            user.is_active = False
            user.save()


            Extendeduser.objects.create(user = user,counter = 0)

            domain = get_current_site(request).domain
            mail_subject = 'Activate your account'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_token.make_token(user)
            to_email = serializer.data['email']
            from_mail = settings.EMAIL_HOST_USER
            activate_link = reverse('activate',kwargs = {'uidb64':uid,'token':token})
            activate_link = '/'.join(activate_link.split('/')[2:])
            message = f"Hi ,Please click on the link to confirm your registration,http://{ domain }/{activate_link}"

            send_mail(mail_subject, message, from_mail, [to_email],fail_silently=False)
            

            data = {
                'user':serializer.data,
                'info': "Please confirm your email address to complete the registration"
            }

            return Response(data,status = status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ActivateView(GenericAPIView):
    
    def get(self,request,uidb64,token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = uid)
        except (ValueError,OverflowError,User.DoesNotExist):
            user = None
        
        if user and account_token.check_token(user,token):
            user.is_active = True
            user.save()
            data = {
                'info' : "Thank you for your email confirmation. Now you can login your account."
            }
            return Response(data,status = status.HTTP_200_OK)
        
        data = {
            "info":"Activation Link is invalid"
        }
        return Response(data,status = status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request):
        serializer = LoginSerializer(data = request.data)

        if not serializer.is_valid():
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        
        email = request.data.get('email','')
        password = request.data.get('password','')

        
        # user with email id always exists as serializer is valid
        user = User.objects.get(email = email)

        #Authenticated User
        if user.check_password(password):
            #Not considered Unsuccessful Attempt
            if not user.is_active:
                return Response({
                    'info':"Account is in verification state. Please verify",
                    },status = status.HTTP_401_UNAUTHORIZED)

            #Account in locked state
            if user.extendeduser.counter == 5:
                Loginhistory.objects.create(user = user,is_success = False)
                return Response({'info':'Account has been locked. Please reset your password by clicking Forgot Password.'},status=status.HTTP_423_LOCKED)


            auth_token = jwt.encode({
                'username':user.username
            },settings.JWT_SECRET_KEY)

            #Send back

            serializer = UserSerializer(user)

            data = {
                'user':serializer.data,
                'token':auth_token
            }
            
            #Successful Login Attempt, also resets counter 
            update_last_login(None,user)
            user.extendeduser.counter = 0
            user.extendeduser.save()
            Loginhistory.objects.create(user = user,is_success = True)
            return Response(data,status = status.HTTP_200_OK)

        
        #Unsuccessful Login Attempt
        Loginhistory.objects.create(user = user,is_success = False)

        if user.extendeduser.counter == 5:  
            return Response({'info':'Account has been locked. Please reset your password by clicking Forgot Password.'},status=status.HTTP_423_LOCKED)

        user.extendeduser.counter += 1
        user.extendeduser.save()
        

        return Response({'info':'Invalid Credentials'},status = status.HTTP_401_UNAUTHORIZED)

class ResetView(GenericAPIView):
    serializer_class = ResetSerializer

    def post(self,request):
        serializer = ResetSerializer(data = request.data)

        if serializer.is_valid():
            user = User.objects.get(email = serializer.data['email'])
        
            domain = get_current_site(request).domain
            mail_subject = 'Password Reset'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_token.make_token(user)
            to_email = serializer.data['email']
            from_mail = settings.EMAIL_HOST_USER
            activate_link = reverse('passwordreset',kwargs = {'uidb64':uid,'token':token})
            activate_link = '/'.join(activate_link.split('/')[2:])
        
        
            message = f"Hi ,Please click on the link to reset your password,http://{ domain }/{activate_link}"
            
            
            send_mail(mail_subject, message, from_mail, [to_email],fail_silently=False)
            

            data = {
                'user':serializer.data,
                'info': "Password Reset Link has been sent. Check your Inbox!"
            }

            return Response(data,status = status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def get(self,request,uidb64,token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = uid)
        except (ValueError,OverflowError,User.DoesNotExist):
            user = None
        
        if user and account_token.check_token(user,token):

            data = {
                'info' : "Enter a new password!"
            }
            return Response(data,status = status.HTTP_200_OK)
        
        data = {
            "info":"Password Reset Link is invalid"
        }
        return Response(data,status = status.HTTP_400_BAD_REQUEST)
    
    def post(self,request,uidb64,token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = uid)
        except (ValueError,OverflowError,User.DoesNotExist):
            user = None
        
        if user and account_token.check_token(user,token):

            serializer = PasswordResetSerializer(data = request.data)

            if not serializer.is_valid():
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
            
            
            user.set_password(serializer.data['password'])
            user.extendeduser.counter = 0
            user.extendeduser.save()
            user.save()
            
            return Response({'info':"Password has been successfully changed."},status=status.HTTP_200_OK)

        return Response({"info":"Password Reset Link is invalid"},status = status.HTTP_400_BAD_REQUEST)
