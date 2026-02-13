from db.session import init_db_on_start_up
from fastapi import FastAPI
from api.routers.nosql.products_images import router as P_router
from api.routers.nosql.blueprints_images import router as B_router
from api.routers.products import router as product_router
import uvicorn

try:
    app = FastAPI(on_startup=[init_db_on_start_up],
                on_shutdown=[])

    # TODO Добавить импорты роутеров

    # EXEMPLE: app.include_router(router)
    app.include_router(P_router)
    app.include_router(B_router)
    app.include_router(product_router)
    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)

except Exception as e:
    # TODO сделать логирование!!
    pass