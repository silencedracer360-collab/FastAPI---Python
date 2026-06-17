from fastapi import APIRouter, HTTPException
from app.listas import listas_clientes
from app.model.cliente import *
from ..conexion_bd import Sesion_dependencia
from sqlmodel import select

router = APIRouter(
        prefix="/clientes",
        tags=["Clientes"]
)

# ===================================
# CRUD CLIENTES
# ===================================


@router.get("/", response_model=list[Cliente])
async def listar_cliente(sesion: Sesion_dependencia):
    list_cli = sesion.exec(select(Cliente)).all()
    return list_cli


@router.get("/{id}", response_model=Cliente)
async def listar_cliente_id(id: int, mi_sesion: Sesion_dependencia):

    for cliente in listas_clientes:

        if cliente.id == id:
            return cliente
    raise HTTPException(status_code=400, detail= f"El cliente con ID {cliente.id}, no existe.")

@router.post("/", response_model=Cliente)
async def crear_cliente(datos_cliente: ClienteCrear, mi_sesion: Sesion_dependencia):

    cliente_validado = Cliente.model_validate(
        datos_cliente.model_dump()
    )

    mi_sesion.add(cliente_validado)
    mi_sesion.commit()
    mi_sesion.refresh(cliente_validado)
    return cliente_validado


@router.put("/{id}")
async def editar_cliente(
    id: int,
    datos_cliente: ClienteEditar,
    mi_sesion: Sesion_dependencia
):

    for i, cliente in enumerate(listas_clientes):

        if cliente.id == id:

            cliente_val = Cliente.model_validate(
                datos_cliente.model_dump()
            )

            cliente_val.id = id

            listas_clientes[i] = cliente_val

            return {
                "mensaje": "Cliente actualizado",
                "cliente": cliente_val
            }

    return {"error": "Cliente no encontrado"}


@router.delete("/{id}")
async def eliminar_cliente(id: int, mi_sesion: Sesion_dependencia):

    for i, cliente in enumerate(listas_clientes):

        if cliente.id == id:

            nombre = cliente.nombre

            del listas_clientes[i]

            return {
                "mensaje": f"Cliente {nombre} eliminado"
            }

    return {"error": "Cliente no encontrado"}
