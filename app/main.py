from fastapi import FastAPI
import uvicorn

from app.imei import views
from app.users import views

app = FastAPI()
app.include_router(router=views.router)
app.include_router(router=views.router)


if __name__ == '__main__':
    uvicorn.run(app="app.main:app", reload=True)