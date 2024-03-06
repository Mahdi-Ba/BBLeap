from area.router import router as area_route
from customers.router import router as customers_route



def include_router(app):
    app.include_router(area_route)
    app.include_router(customers_route)


