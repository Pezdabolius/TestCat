from django.test import TestCase
import pytest
from rest_framework.test import APIClient
import pytest_django
from django.urls import reverse
from .models import Kitten
from django.contrib.auth.models import User


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username='admin', password='password')


@pytest.fixture
def user2():
    return User.objects.create_user(username='test', password='password')


@pytest.fixture
def kittens(user):
    Kitten.objects.create(owner=user, name='Muffin', breed='persian',
                          color='green', age='3', description='1')
    Kitten.objects.create(owner=user, name='Maffin', breed='bengal',
                          color='green', age='3', description='1')


@pytest.fixture
def kitten(user):
    return Kitten.objects.create(owner=user, name='Fuffin', breed='bengal',
                                 color='green', age='3', description='1')


@pytest.mark.django_db
def test_get_list_kittens(client, kittens):
    response = client.get(reverse('list_kittens'))
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_post_list_kittens(client, user):
    data = {'name': 'Fusa', 'breed': 'bengal', 'age': '3', 'description': '1',
            'owner': user.id, 'color': 'green'}
    response = client.post(reverse('list_kittens'), data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_list_breeds(client, kittens):
    response = client.get(reverse('list_breed'))
    assert response.status_code == 200
    assert response.data['breeds'] == ['bengal', 'persian']
    assert response.data['breeds'][0] == 'bengal'


@pytest.mark.django_db
def test_kitten_detail_get(client, kitten):
    response = client.get(reverse('kitten_detail', kwargs={'pk': kitten.pk}))
    assert response.status_code == 200
    assert response.data['name'] == kitten.name


@pytest.mark.django_db
def test_kitten_detail_patch_user(client, kitten, user):
    client.force_authenticate(user=user)
    data = {'name': 'Fatech'}
    response = client.patch(reverse('kitten_detail', kwargs={'pk': kitten.pk}), data)
    assert response.status_code == 200
    assert response.data['name'] != kitten.name
    kitten.refresh_from_db()
    assert response.data['name'] == kitten.name


@pytest.mark.django_db
def test_kitten_detail_patch_user2(client, kitten, user2):
    client.force_authenticate(user=user2)
    data = {'name': 'Fatech'}
    response = client.patch(reverse('kitten_detail', kwargs={'pk': kitten.pk}), data)
    assert response.status_code == 403