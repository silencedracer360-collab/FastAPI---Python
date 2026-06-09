from fastapi import APIRouter
from app.conexion_bd import listas_clientes
from app.model.cliente import *

router = APIRouter(
        prefix="/clientes",
        tags=["Clientes"]
)

# ===================================
# CRUD CLIENTES
# ===================================


@router.get("/")
async def listar_cliente():

    if len(listas_clientes) == 0:
        return {"mensaje": "No hay clientes registrados"}

    return listas_clientes


@router.get("/{id}")
async def listar_cliente_id(id: int):

    for cliente in listas_clientes:

        if cliente.id == id:
            return cliente

    return {"error": "Cliente no encontrado"}


@router.post("/", response_model=Cliente)
async def crear_cliente(datos_cliente: ClienteCrear):

    cliente_validado = Cliente.model_validate(
        datos_cliente.model_dump()
    )

    cliente_validado.id = len(listas_clientes) + 1

    listas_clientes.append(cliente_validado)

    return cliente_validado


@router.put("/{id}")
async def editar_cliente(
    id: int,
    datos_cliente: ClienteEditar
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
async def eliminar_cliente(id: int):

    for i, cliente in enumerate(listas_clientes):

        if cliente.id == id:

            nombre = cliente.nombre

            del listas_clientes[i]

            return {
                "mensaje": f"Cliente {nombre} eliminado"
            }

    return {"error": "Cliente no encontrado"}
