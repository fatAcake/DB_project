from db.session import init_db_on_start_up
from fastapi import FastAPI
import uvicorn

try:
    app = FastAPI(on_startup=[init_db_on_start_up],
                on_shutdown=[])

    # TODO Добавить импорты роутеров

    # EXEMPLE: app.include_router(router)

    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)

except Exception as e:
    # TODO сделать логирование!!
    pass