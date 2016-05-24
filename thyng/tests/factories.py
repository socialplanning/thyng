from django.contrib.auth import get_user_model
from django.utils.text import slugify
import factory
import factory.fuzzy

from thyng import models


class ProjectFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Project

    title = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: "user%d" % n)
    email = factory.LazyAttribute(lambda o: '%s@example.org' % o.username)
    password = factory.PostGenerationMethodCall('set_password', 'password')

    is_staff = False
    is_active = True

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for group in extracted:
                self.groups.add(group)
