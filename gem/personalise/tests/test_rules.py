import pytest

from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from django.test.client import Client


from gem.personalise.rules import GemUserProfileRule

@pytest.mark.django_db
class TestGemUserProfileRule(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()

        # Fabricate a request with a logged-in user
        # so we can use it to test users
        user = get_user_model().objects \
                               .create_user(username='tester',
                                            email='tester@example.com',
                                            password='tester')
        self.request = self.request_factory.get('/')
        self.request.user = user

    def set_user_to_male(self):
        # Set user to male
        self.request.user.gem_profile.gender = 'm'
        self.request.user.save()

    def set_user_to_female(self):
        self.request.user.gem_profile.gender = 'f'
        self.request.user.save()

    def set_user_to_unspecified(self):
        self.request.user.gem_profile.gender = '-'
        self.request.user.save()

    def test_unspecified_passes_unspecified_rule(self):
        self.set_user_to_unspecified()
        unspecified_rule = GemUserProfileRule(field='gender', value='-')

        self.assertTrue(unspecified_rule.test_user(self.request))

    def test_male_passes_male_rule(self):
        self.set_user_to_male()
        male_rule = GemUserProfileRule(field='gender', value='m')

        self.assertTrue(male_rule.test_user(self.request))

    def test_female_passes_female_rule(self):
        self.set_user_to_female()
        female_rule = GemUserProfileRule(field='gender', value='f')

        self.assertTrue(female_rule.test_user(self.request))

    def test_unspecified_fails_female_rule(self):
        self.set_user_to_unspecified()
        female_rule = GemUserProfileRule(field='gender', value='f')

        self.assertFalse(female_rule.test_user(self.request))

    def test_female_fails_unspecified_rule(self):
        self.set_user_to_female()
        unspecified_rule = GemUserProfileRule(field='gender', value='-')

        self.assertFalse(unspecified_rule.test_user(self.request))

    def test_male_fails_unspecified_rule(self):
        self.set_user_to_male()
        unspecified_rule = GemUserProfileRule(field='gender', value='-')

        self.assertFalse(unspecified_rule.test_user(self.request))

    def test_unexisting_profile_field_fails(self):
        rule = GemUserProfileRule(field='not_existing_field', value='l')

        self.assertFalse(rule.test_user(self.request))
