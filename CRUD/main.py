from fastapi import FastAPI
from admin.apis import routers as AdminRouter
from tortoise.contrib.fastapi import register_tortoise




app=FastAPI()
app.include_router(AdminRouter.router,tags=["Admin"])



@app.get("/")
def read_root():
    return {"Hello": "World"}

register_tortoise(
    app,
    db_url='mysql://root@localhost:3306/test',
    modules={'models': ['admin.apis.models','aerich.models']},
    generate_schemas=True,
    add_exception_handlers=True
)    

@app.get("/login/")
def login():
    return {"data":"login"}