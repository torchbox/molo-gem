from django.contrib.auth import get_user_model
from molo.core.backends import MoloModelBackend

UserModel = get_user_model()


class GemModelBackend(MoloModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        if username is not None:
            try:
                user = UserModel.objects.get(
                    gem_profile__migrated_username=username,
                    profile__site=request.site)
                username = user.username
            except UserModel.DoesNotExist:
                UserModel().set_password(password)

        return super(GemModelBackend, self).authenticate(
            request=request, username=username, password=password, **kwargs)
