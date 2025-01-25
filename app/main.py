from fastapi import FastAPI
import uvicorn

from routers import user

app = FastAPI()
app.include_router(router=user.router)


if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)