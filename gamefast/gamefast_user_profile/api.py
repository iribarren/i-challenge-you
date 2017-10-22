from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from django.contrib.auth import get_user_model # If used custom user model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


from .serializers import UserSerializer


class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
    ]
    serializer_class = UserSerializer


class GetUserView(RetrieveAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UserSerializer
    lookup_field = 'pk'
    queryset = User.objects.all()

    def get_object(self):
        queryset = User.objects.filter(pk=self.request.user.pk)
        obj = queryset.get(pk=self.request.user.pk)
        self.check_object_permissions(self.request, obj)
        return obj

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
