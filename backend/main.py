from db.session import init_db_on_start_up
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.logs_router import router as logs_router
from api.routers.passportdata_router import router as passportdata_router

from api.routers.nosql.products_images import router as P_router
from api.routers.nosql.blueprints_images import router as B_router
from api.routers.products import router as product_router
from api.routers.quantity_products import router as qp_router
from api.routers.blueprints_router import router as blueprint_router
from api.routers.transactions import router as transaction_router
from api.routers.feedback import router as feedback_router
from api.routers.confirm_passport_data import router as cpd_router
from api.routers.users_router import router as user_router
from api.routers.roles_router import router as roles_router
import uvicorn

try:
    app = FastAPI(on_startup=[init_db_on_start_up],
                on_shutdown=[])
    app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  
        "http://localhost:5173",   
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)
    app.include_router(P_router)
    app.include_router(B_router)

    app.include_router(logs_router)
    app.include_router(passportdata_router)

    app.include_router(product_router)
    app.include_router(qp_router)
    app.include_router(blueprint_router)
    app.include_router(transaction_router)
    app.include_router(feedback_router)
    app.include_router(cpd_router)
    app.include_router(user_router)
    app.include_router(roles_router)
    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8000)

except Exception as e:
    # TODO сделать логирование!!
    pass