from core.routes import include_router
from core.settings import settings
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

description = """
Welcome to the GEO SATELLITE API web service! 🚀

To get started, you'll need to create a customer account. Once you've created your account, you can log in using your username and password to access all the API features related to geospatial data.

My name is Mahdi Bahari, and I'm committed to crafting an incredibly beautiful experience for you as you navigate through our service.

I'm eager to join your group and contribute my skills and passion to our shared goals. Please consider this as my enthusiastic request to become part of your team. Together, we can achieve great things and make a meaningful impact in the world of geospatial technology.

Thank you for considering me, and I look forward to the opportunity to work alongside you.

Best regards,
Mahdi Bahari


"""


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, debug=settings.DEBUG,
                  description=description,summary='work correctly',
                  terms_of_service="https://github.com/Mahdi-Ba",
                  contact={
                      "name": "Mahdi Bahari",
                      "email": "baharimahdi93@gmail.com",
                  },
                  license_info={
                      "name": "Apache 2.0",
                      "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
                  },
                  )
    include_router(app)
    return app


app = start_application()
app.mount("/media", StaticFiles(directory="media"), name="media")
@app.get("/media/{filename}")
async def serve_media(filename: str):
    return {"filename": filename}





import uvicorn

# if __name__ == '__main__':
#     uvicorn.run(app, host='0.0.0.0', port=8000)



