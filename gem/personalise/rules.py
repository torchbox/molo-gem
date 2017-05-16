from django.utils.translation import ugettext_lazy as _
from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel

from personalisation.rules import AbstractBaseRule

from gem.models import GemUserProfile


ALLOWED_FIELDS = ['gender']


def get_profile_fields_for_personalisation(allowed_fields):
    """Get a tuple of choices for profile fields in personaliastion."""
    model_fields = GemUserProfile._meta.fields

    fields = [f for f in model_fields if f.name in allowed_fields]

    return tuple([(field.name, field.verbose_name.title()) for field in fields])


class GemUserProfileRule(AbstractBaseRule):
    field = models.CharField(
        max_length=255,
        choices=get_profile_fields_for_personalisation(ALLOWED_FIELDS)
    )
    value = models.CharField(max_length=255)

    panels = [
        FieldPanel('field'),
        FieldPanel('value')
    ]

    def __init__(self, *args, **kwargs):
        super(GemUserProfileRule, self).__init__(*args, **kwargs)

    def __str__(self):
        return _('GEM Profile Data')

    def description(self):
        description = {
            'title': _('Based on profile data'),
            'value': _('"{}" is "{}"').format(
                self.field,
                self.value
            ),
        }

        return description

    def test_user(self, request):
        # If gem profile has attribute test it
        if hasattr(request.user.gem_profile, self.field):
            return getattr(request.user.gem_profile, self.field) == self.value

        # Otherwise just fail
        return False

