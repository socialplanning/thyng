import factory
import factory.fuzzy

from thyng import models


class ProjectFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Project

    title = factory.fuzzy.FuzzyText()
