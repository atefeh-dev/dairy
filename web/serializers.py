from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import *
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        """create new user """

        print("im here in create ")
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """ update user model """

        instance.password = validated_data.get('password', instance.password)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.save()
        return instance