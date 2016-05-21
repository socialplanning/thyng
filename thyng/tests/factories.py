from django.utils.text import slugify
import factory
import factory.fuzzy

from thyng import models


class ProjectFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Project

    title = factory.fuzzy.FuzzyText()
    slug = factory.LazyAttribute(lambda obj: slugify(obj.title))
