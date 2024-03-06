import asyncio
import json
from datetime import timedelta
from typing import List
import requests
from fastapi import Depends, APIRouter, status, HTTPException, Request
from shapely.geometry import shape
from sqlalchemy.orm import Session
from area.models.area_models import *
from area.schemmas.schemas import *
from area.services.service import query_stac_api
from core.db import get_db, redis_client
from customers.models.customers_models import Customer
from customers.router import get_current_user

router = APIRouter(
    prefix="/v1/area",
    tags=["Polygon"],
    responses={404: {"description": "Not founds"}},
)


@router.post("/")
async def create_area(area: AreaBaseCreate, db: Session = Depends(get_db),
                      current_user: Customer = Depends(get_current_user)) -> AreaResponse:
    '''
    below is simple example can test it

         {
          "name": "Example Field",
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
        }
    '''

    geojson_geometry = area.geometry.dict()
    try:
        shapely_geometry = shape(geojson_geometry)
        # Convert the shapely geometry to WKT
        wkt_geometry = shapely_geometry.wkt
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="error please submit correct data")

    db_field = Area(name=area.name, geometry=wkt_geometry)
    db.add(db_field)
    db.commit()
    db.refresh(db_field)
    return AreaResponse.from_db(db_field)


@router.get("/")
async def get_areas(db: Session = Depends(get_db), current_user: Customer = Depends(get_current_user)) -> List[
    AreaResponse]:
    areas = db.query(Area).all()
    return [AreaResponse.from_db(area) for area in areas]


@router.get("/{uuid}")
async def get_area_by_uuid(uuid: UUID, db: Session = Depends(get_db),
                           current_user: Customer = Depends(get_current_user)) -> AreaResponse:
    if data := redis_client.get(str(uuid)):
        client_report = json.loads(data)
        return client_report
    area = db.query(Area).filter(Area.uuid == uuid).first()
    if area is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")
    return AreaResponse.from_db(area)


@router.post("/intersecting-area", response_model=List[AreaResponse])
async def get_intersecting_areas(geometry: Geometry, db: Session = Depends(get_db)):
    '''
    this is an amazing reference https://postgis.net/docs/reference.html below is simple example can test it

             {
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
    '''

    geojson_geometry = geometry.dict()
    try:
        shapely_geometry = shape(geojson_geometry)
        # Convert the shapely geometry to WKT
        wkt_geometry = shapely_geometry.wkt
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="error please submit correct data")
    intersecting_fields = db.query(Area).filter(Area.geometry.ST_Intersects(wkt_geometry)).all()
    return [AreaResponse.from_db(field) for field in intersecting_fields]


@router.post("/get-newest-image/")
async def get_newest_image(geometry: Geometry) -> RecentImageResponse:
    '''
    Point 1: Near Lands End
    Point 2: Near Mission District
    Point 3: Near Fisherman's Wharf
    Point 4: Across the Golden Gate Bridge
    Closing the polygon by repeating the first point

            {
              "type": "Polygon",
              "coordinates": [
                [
                   [-122.514426, 37.708075],
                   [-122.358093, 37.708075],
                   [-122.358093, 37.810835],
                   [-122.514426, 37.810835],
                   [-122.514426, 37.708075]
                ]
              ]
            }
    '''
    try:
        print(geometry.dict())
        href, updated_at = await query_stac_api(geometry.dict())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="bad event happened !!")

    if not href:  # Check if no images were found
        raise HTTPException(status_code=404, detail="No images found for the given polygon.")

    return {"href": href, "updated_at": updated_at}


@router.get("/get-newest-image/{uuid}")
async def get_newest_image_by_uuid(uuid: UUID, db: Session = Depends(get_db),
                                   current_user: Customer = Depends(get_current_user)) -> RecentImageResponse:
    if data := redis_client.get(f"{uuid}_image"):
        client_report = json.loads(data)
        return client_report
    area = db.query(Area).filter(Area.uuid == uuid).first()

    if area is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Area not found")
    try:
        res = AreaResponse.from_db(area).dict()
        converted_coordinates = [[list(coord) for coord in polygon] for polygon in
                                 res.get('geometry').get('coordinates')[0]]
        data = {
            "type": res.get('geometry').get('type'),
            "coordinates": converted_coordinates
        }
        href, updated_at = await query_stac_api(data)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad event happened !!")

    if not href:  # Check if no images were found
        raise HTTPException(status_code=404, detail="No images found for the given polygon.")
    raw_body = {"href": href, "updated_at": updated_at}
    redis_client.set(f"{uuid}_image", json.dumps(raw_body), ex=timedelta(minutes=1))
    return raw_body
