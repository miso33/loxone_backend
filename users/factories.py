import factory
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: 'User{0}'.format(n + 110))
    email = factory.Sequence(lambda n: 'name{0}@email.com'.format(n + 110))
    password = factory.Sequence(lambda n: 'password{0}'.format(n + 110))

    class Meta:
        model = UserModel
