from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel

from personalisation.rules import AbstractBaseRule

from molo.profiles.models import UserProfile


def get_profile_fields_for_personalisation(allowed_fields, models):
    """
    Get a tuple of choices for profile fields in personaliastion.
    """
    choices = []

    for model in models:
        for field in model._meta.fields:
            if '{}__{}'.format(model._meta.model_name, field.name) in allowed_fields:
                choices += [(
                    '{}__{}'.format(model._meta.model_name, field.name),
                    '{} - {}'.format(model._meta.verbose_name.title(),
                                     field.verbose_name.title())
                )]

    return choices

FIELD_MODELS = [User, UserProfile]
ALLOWED_FIELDS = [
    'user__date_joined',
    'userprofile__date_of_birth',
    'userprofile__gender'
]
CHOICES = get_profile_fields_for_personalisation(ALLOWED_FIELDS, FIELD_MODELS)

class ProfileDataRule(AbstractBaseRule):
    field = models.CharField(
        max_length=255,
        choices=CHOICES
    )
    value = models.CharField(max_length=255)

    panels = [
        FieldPanel('field'),
        FieldPanel('value')
    ]

    def __init__(self, *args, **kwargs):
        super(ProfileDataRule, self).__init__(*args, **kwargs)

    def __str__(self):
        return _('GEM Profile Data')

    def description(self):
        field_name = ''

        for choice in CHOICES:
            if choice[0] == self.field:
                field_name = choice[1]
                break

        description = {
            'title': _('Based on profile data'),
            'value': _('{}: "{}"').format(
                field_name or self.field,
                self.value
            ),
        }

        return description

    def test_user(self, request):
        if not request.user.is_authenticated():
            return False

        model_name, field_name = self.field.split('__', 1)

        if model_name == 'userprofile':
            instance = request.user.profile
        elif model_name == 'user':
            instance = request.user
        else:
            raise NotImplementedError('{} not implemented on {}.test_user.'.format(
                model_name,
                type(self).__name__
            ))

        # Check whether given field_name exists
        if hasattr(instance, field_name):
            return getattr(instance, field_name) == self.value

        # Otherwise just fail
        return False

