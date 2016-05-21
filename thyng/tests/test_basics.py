from django.test import TestCase, override_settings

class BasicTest(TestCase):

    def test_foo(self):
        self.assertEquals("foo", "foo")
