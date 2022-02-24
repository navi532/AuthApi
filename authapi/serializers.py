
import email
from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length = 8,max_length = 65,write_only = True)
    confirm_password = serializers.CharField(min_length = 8,max_length = 65,write_only = True)
    email = serializers.EmailField(min_length = 5,max_length = 255)
    first_name = serializers.CharField(min_length = 2,max_length = 255)
    last_name = serializers.CharField(min_length = 2,max_length = 255)


    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password','confirm_password']

    #.is_valid()
    def validate(self, attrs):
        if User.objects.filter(email = attrs.get('email','')).exists():
            raise serializers.ValidationError(
                {
                    'email':'Email already exists'
                }
            )
        if attrs.get('password','')!= attrs.get('confirm_password',''):
            raise serializers.ValidationError(
                {
                    'confirm_password': "Password Fields doesn't match. Try Again"
                }
            )
        return super().validate(attrs)

    #.save()
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length = 5,max_length = 255)
    password = serializers.CharField(min_length = 8,max_length = 65,write_only = True)

    class Meta:
        model = User
        fields = ['email','password']
    
    #.is_valid()
    def validate(self, attrs):
        if not User.objects.filter(email = attrs.get('email','')).exists():
            raise serializers.ValidationError(
                {
                    'email':"Email doesn't exists."
                }
            )

        return super().validate(attrs)

class ResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length = 5,max_length = 255)

    class Meta:
        model = User
        fields = ['email']
    
    #.is_valid()
    def validate(self, attrs):
        if not User.objects.filter(email = attrs.get('email','')).exists():
            raise serializers.ValidationError(
                {
                    'email':"Email doesn't exists."
                }
            )

        return super().validate(attrs)

class PasswordResetSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(min_length = 8,max_length = 65)
    confirm_password = serializers.CharField(min_length = 8,max_length = 65)

    class Meta:
        model = User
        fields = ['password','confirm_password']
    
    #.is_valid()
    def validate(self, attrs):

        if attrs.get('password','')!= attrs.get('confirm_password',''):
            raise serializers.ValidationError(
                {
                    'confirm_password': "Password Fields doesn't match. Try Again"
                }
            )
        return super().validate(attrs) 
