from django.test import TestCase, override_settings

class BasicTest(TestCase):

    def test_homepage(self):
        rsp = self.client.get("/")
        self.assertEqual(200, rsp.status_code)
        self.assertIn("Thyng", rsp.content)
