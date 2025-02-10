from fastapi import FastAPI
import uvicorn

from app.users import views as users_views
from app.auth import views as auth_views
from app.imei import views as imei_views


app = FastAPI()
app.include_router(router=auth_views.router)
app.include_router(router=users_views.router)
app.include_router(router=imei_views.router)

if __name__ == '__main__':
    uvicorn.run(app="app.main:app", reload=True)