import pytest
from httpx import AsyncClient
from area.models.area_models import Area
from test_main import get_token_header
from conftest import app, TestingSessionLocal


@pytest.mark.anyio
@pytest.mark.dependency()
async def test_create_Area(get_token_header):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/area/", headers=get_token_header,
                                 json={
                                     "name": "first_test",
                                     "geometry": {
                                         "type": "Polygon",
                                         "coordinates": [
                                             [
                                                 [100.0, 0.0],
                                                 [101.0, 0.0],
                                                 [101.0, 1.0],
                                                 [100.0, 1.0],
                                                 [100.0, 0.0]
                                             ]
                                         ]
                                     }
                                 })
        assert response.status_code == 200, response.json()
        response = await ac.get("/v1/area/", headers=get_token_header, params={'uuid': response.json()['uuid']})
        assert response.status_code == 200, response.json()


@pytest.mark.anyio
@pytest.mark.dependency(depends=["test_create_Area[trio]"])
async def test_read_items(get_token_header):
    db = TestingSessionLocal()
    res = db.query(Area).first()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/v1/area/", headers=get_token_header)
        assert response.status_code == 200, response.json()
        assert isinstance(response.json(), list)


@pytest.mark.anyio
@pytest.mark.dependency(depends=["test_create_Area[trio]"])
async def test_read_item_with_uuid(get_token_header):
    db = TestingSessionLocal()
    res = db.query(Area).first()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/v1/area/{res.uuid}", headers=get_token_header)
        assert response.status_code == 200, response.json()
        assert response.json()['uuid'] == str(res.uuid)


@pytest.mark.anyio
@pytest.mark.dependency(depends=["test_create_Area[trio]"])
async def test_read_item_with_intersecting_areas(get_token_header):
    db = TestingSessionLocal()
    res = db.query(Area).first()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/area/intersecting-area", headers=get_token_header, json={
            "type": "Polygon",
            "coordinates": [
                [
                    [100.0, 0.0],
                    [101.0, 0.0],
                    [101.0, 1.0],
                    [100.0, 1.0],
                    [100.0, 0.0]
                ]
            ]
        }
                                 )
        assert response.status_code == 200, response.json()
        assert isinstance(response.json(), list)


@pytest.mark.anyio
@pytest.mark.dependency(depends=["test_create_Area[trio]"])
async def test_get_image_areas(get_token_header):
    db = TestingSessionLocal()
    res = db.query(Area).first()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/v1/area/get-newest-image/", headers=get_token_header, json={
            "type": "Polygon",
            "coordinates": [
                [
                    [100.0, 0.0],
                    [101.0, 0.0],
                    [101.0, 1.0],
                    [100.0, 1.0],
                    [100.0, 0.0]
                ]
            ]
        }
                                 )
        assert response.status_code == 200, response.json()
        assert isinstance(response.json(), dict)

@pytest.mark.anyio
@pytest.mark.dependency(depends=["test_create_Area[trio]"])
async def test_get_image_areas_by_uuid(get_token_header):
    db = TestingSessionLocal()
    res = db.query(Area).first()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/v1/area/get-newest-image/{res.uuid}", headers=get_token_header)
        assert response.status_code == 200, response.json()
        assert isinstance(response.json(), dict)