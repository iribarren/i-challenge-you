from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model # If used custom user model

from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator
from django.db.models.fields import EmailField



UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    #password = serializers.CharField(write_only=True)
    #email = EmailField(allow_blank=True, label='Email address', max_length=254, required=False,validators=[UniqueValidator(queryset=User.objects.all())])
    email = EmailField(max_length=254,validators=[UniqueValidator(queryset=User.objects.all())])

    def create(self, validated_data):

        user = UserModel.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = UserModel
        fields = ('username','email','first_name','last_name', 'password')
