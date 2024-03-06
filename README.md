# GEO Satellite  FastAPI Application
#####  This is a FastAPI application that provides an API for managing Polygon data.

## Production
- Ensure no port conflicts exist on your machine.
- Navigate to the project directory containing the docker-compose.yml file.
- Run the following command:
```bash
docker-compose up 
```
- wait to this message appears in terminal "Application startup complete."
- Once the containers are up and running, access the API documentation by visiting http://0.0.0.0:8000/docs#/.
- The first step is to create a customer account. Afterward, proceed to log in using the provided username and password.
- Explore and utilize the available endpoints as needed.

## Stage

## Installation
To install the dependencies, run the following command:

```bash
pip install -r requirements.txt
```
This will install all the required dependencies for the application.

## Project Configuration
The application can be configured by editing the [env.py](alembic%2Fenv.py) file in core directory The following settings can be configured:
- uncomment load_dotenv in  [settings.py](core%2Fsettings.py) and fill [.env](core%2F.env)
- DATABASE_URL: The URL of the database used by the application.
- DEBUG: Whether to run the application in debug mode.
## Running the Application

To start the application, run the following command:

``` bash
uvicorn main:app --reload
```


This will start the application on http://localhost:8000/.

## API Docs Endpoints
To view the API documentation, navigate to http://localhost:8000/docs in a web browser. This will open the Swagger UI, which provides documentation for all the API endpoints.

### Alembic Migration
Config DB line 63  [alembic.ini](alembic.ini)

In new model you should add model in [env.py](alembic%2Fenv.py) file above this section
``` python
...
import model
...
target_metadata = Base.metadata
```
Then run below command to create migration or alter then migrate
``` bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

> **⚠ Warning**
> Do't rename model class name I'm sure remove table


### Routing
Add routing in [routes.py](core%2Froutes.py)
```python
def include_router(app):
    ...
    ...
    app.include_router($YOUR_ROUTE)
```


## Deployment
To deploy the application to a production environment, follow these steps:
Update the .env file with the appropriate production settings.
Set the DEBUG environment variable to False.
in production mode You can set many parameters such as workers

``` bash
uvicorn main:app  --workers 4 
```


## Test
at the first You should create Fake DataBase and set DATABASE_TEST_URL in [.env](core%2F.env) 
``` bash
pytest -p no:warnings -v -s
```

