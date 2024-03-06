from test_main import real_super_user
from conftest import app
from httpx import AsyncClient
import pytest
from test_main import get_token_header


@pytest.mark.anyio
async def test_update_user(get_token_header):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/customers/users", headers=get_token_header, json={
            'username': real_super_user['username'],
            'is_active': True,
            'is_superuser': True
        })
        assert response.status_code == 200
        assert response.json()['username'] == real_super_user['username']


@pytest.mark.anyio
async def test_get_me_info(get_token_header):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/v1/customers/me", headers=get_token_header)
        assert response.status_code == 200
        assert response.json()['username'] == real_super_user['username']


