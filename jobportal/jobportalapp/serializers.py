from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User




class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields ="__all__"



class UserSerializer(serializers.ModelSerializer):


    class Meta:
        model = User
        fields = ('user_name', 'mail', 'password')

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class JobProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=JobProfile
        fields="__all__"
