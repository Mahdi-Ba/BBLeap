import pytest
from customers.router import get_current_super_user, get_current_user
from conftest import app
from httpx import AsyncClient


class User:
    def __init__(self):
        self.username = 'fake_super_user'
        self.is_active = True
        self.is_superuser = True


def override_get_current_super_user():
    return User()


real_super_user = {
    'username': 'test',
    'password': 'test',
    'is_active': True,
    'is_superuser': True
}


@pytest.mark.anyio
async def test_create_user():
    """below for first super_user created because first super_user create manually """
    app.dependency_overrides[get_current_super_user] = override_get_current_super_user
    app.dependency_overrides[get_current_user] = override_get_current_super_user
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/customers/users", json=real_super_user)
        assert response.status_code == 200
        assert response.json()['is_active'] is True
        assert response.json()['is_superuser'] is True

        """Dont need this because I create real first super user in DB"""
        app.dependency_overrides.pop(get_current_super_user, None)
        app.dependency_overrides.pop(get_current_user, None)


@pytest.fixture(scope="function")
async def get_token_header():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/customers/token", data={
            'username': real_super_user['username'],
            'password': real_super_user['password']
        })
        assert response.status_code == 200
        headers = {'Authorization': f"{response.json()['token_type']} {response.json()['access_token']}"}
        return headers