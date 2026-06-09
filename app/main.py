from fastapi import FastAPI
from app.enrutador import clientes, facturas, transacciones
from app.enrutador.facturas import *
from app.enrutador.transacciones import *




app = FastAPI()


app.include_router(clientes.router)
app.include_router(facturas.router)
app.include_router(transacciones.router)


