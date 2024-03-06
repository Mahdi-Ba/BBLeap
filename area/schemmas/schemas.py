from pydantic import BaseModel
from typing import List, Optional
from pydantic.schema import UUID, datetime
from pydantic import BaseModel, validator
from typing import List, Optional
from enum import Enum

from shapely import wkb
from shapely.geometry import shape


class EnumArea(str, Enum):
    """
    you can increase option according shapely package
    linearring
    multipoint
    multilinestring
    multipolygon
    geometrycollection
    """
    Polygon = "Polygon"
    Point = "Point"
    LineString = "LineString"


class Geometry(BaseModel):
    type: EnumArea
    coordinates: List


class AreaBase(BaseModel):
    name: str
    geometry: Geometry


class AreaBaseCreate(AreaBase):
    pass


class AreaResponse(AreaBase):
    id: int
    created_at: datetime
    uuid: UUID

    class Config:
        orm_mode = True

    @classmethod
    def from_db(cls, db_area):
        geojson_geometry = wkb.loads(bytes(db_area.geometry.data))
        geometry = shape(geojson_geometry)
        if geometry.geom_type == 'Polygon':
            coordinates = [[list(geometry.exterior.coords)] + [list(ring.coords) for ring in geometry.interiors]]
        elif geometry.geom_type == 'MultiPolygon':
            coordinates = [
                [[list(polygon.exterior.coords)] + [list(ring.coords) for ring in polygon.interiors] for polygon in
                 geometry]]
        else:
            coordinates = None
        geojson_geometry = {"type": geometry.geom_type, "coordinates": coordinates}
        return cls(
            id=db_area.id,
            name=db_area.name,
            geometry=geojson_geometry,
            created_at=db_area.created_at,
            uuid=db_area.uuid
        )


class RecentImageResponse(BaseModel):
    href: str
    updated_at: datetime
