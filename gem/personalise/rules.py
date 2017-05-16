import datetime
import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel

from molo.profiles.models import UserProfile
from personalisation.rules import AbstractBaseRule

from gem.models import GemUserProfile

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


def get_model_by_name(name):
    return {m._meta.model_name: m for m in FIELD_MODELS}[name]


FIELD_MODELS = [User, UserProfile, GemUserProfile]
ALLOWED_FIELDS = [
    'user__date_joined',
    'userprofile__date_of_birth',
    'gemuserprofile__gender'
]
CHOICES = get_profile_fields_for_personalisation(ALLOWED_FIELDS, FIELD_MODELS)

class ProfileDataRule(AbstractBaseRule):
    OPERATOR_CHOICES = (
        ('lt', _('Less than')),
        ('lte', _('Less than or equal')),
        ('gt', _('Greater than')),
        ('gte', _('Greater than or equal')),
        ('eq', _('Equal')),
        ('neq', _('Not equal')),
        ('old', _('Older than')),
        ('ygr', _('Younger than')),
        ('eqa', _('Of age')),
        ('reg', _('Regex')),
    )

    field = models.CharField(max_length=255, choices=CHOICES)
    operator = models.CharField(max_length=3, choices=OPERATOR_CHOICES)
    value = models.CharField(max_length=255)

    panels = [
        FieldPanel('field'),
        FieldPanel('operator'),
        FieldPanel('value')
    ]

    def __init__(self, *args, **kwargs):
        super(ProfileDataRule, self).__init__(*args, **kwargs)

    def __str__(self):
        return _('GEM Profile Data')

    def clean(self):
        model_name, field_name = self.field.split('__', 1)
        model = get_model_by_name(model_name)
        field = model._meta.get_field(field_name)

        # Deal with regular expression operator
        if self.operator == 'reg':
            # Make sure value is a valid regular expression string
            try:
                re.compile(self.value)
            except re.error as error:
                raise ValidationError({'value': 'Regular expression error: {}'.format(error)})

        # Deal with age opeartors
        elif self.operator == 'old' or self.operator == 'ygr' \
                or self.operator == 'eqa':
            # Works only on DateField
            if not isinstance(field, models.DateField):
                raise ValidationError({
                    'operator': [
                        'You can choose "Of age", "Younger"  or "Older" '
                        'operator only on date and date-time fields.'
                    ]
                })

            try:
                self.value = int(self.value)
            except ValueError:
                raise ValidationError({'value': ['Has to be a whole integer '
                                                 'when using age operators.']})

        # Deal with normal operators
        else:
            # Reassign all errors to the "value" field
            try:
                field.clean(self.value, None)
            except ValidationError as error:
                raise ValidationError({'value': error})

    def description(self):
        field_name = ''

        for choice in CHOICES:
            if choice[0] == self.field:
                field_name = choice[1]
                break

        description = {
            'title': _('Based on profile data'),
            'value': _('"{}" {} "{}"').format(
                field_name or self.field,
                self.get_operator_display(),
                self.value
            )
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
            # Deal with regex operator
            if self.operator == 'reg':
                if re.match(self.value, str(getattr(instance, field_name))) is not None:
                    return True
                else:
                    return False

            # Deal with age operators
            elif self.operator == 'age' or self.operator =='old' \
                    or self.operator == 'ygr':
                date = getattr(instance, field_name)
                python_value = int(self.value)

                # Field has to be a date or date-time
                if not isinstance(date, datetime.date):
                    raise RuntimeError('{} is not a date or datetime instance.')

                # Convert datetime to date if it is a datetime
                date = date.date() if isinstance(date, datetime.datetime) else date

                # Calculate age
                today = timezone.now().date()
                age = today.year - date.year - ((today.month, today.day) < (date.month, date.day))

                if self.operator == 'age':
                    return age == python_value
                elif self.operator == 'ygr':
                    return age < python_value
                elif self.operator == 'old':
                    return age > python_value
                else:
                    raise NotImplementedError('Operator "{}" not implemented on {}.'
                                              'test_user.'.format(self.operator,
                                                                  type(self).__name__))

            # Deal with normal Python operators
            else:
                field = type(instance)._meta.get_field(field_name)
                python_value = field.clean(self.value, None)

                if self.operator == 'lt':
                    return getattr(instance, field_name) < python_value
                elif self.operator == 'lte':
                    return getattr(instance, field_name) <= python_value
                elif self.operator == 'gt':
                    return getattr(instance, field_name) > python_value
                elif self.operator == 'gte':
                    return getattr(instance, field_name) >= python_value
                elif self.operator == 'eq':
                    return getattr(instance, field_name) == python_value
                elif self.operator == 'neq':
                    return getattr(instance, field_name) != python_value

                else:
                    raise NotImplementedError('Operator "{}" not implemented on {}.'
                                              'test_user.'.format(self.operator,
                                                                  type(self).__name__))

        # Otherwise just fail
        return False

