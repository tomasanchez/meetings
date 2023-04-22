"""
Applicant Main File.
"""

import uvicorn

from auth.app.asgi import get_application
from auth.app.settings.uvicorn_settings import UvicornSettings

app = get_application()

if __name__ == "__main__":
    settings = UvicornSettings()

    uvicorn.run(app=settings.APP,
                host=settings.HOST,
                port=settings.PORT,
                reload=settings.RELOAD,
                )
