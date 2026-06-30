from fastapi import APIRouter, HTTPException
from app.model.transacciones import *
from app.model.factura import Factura
from ..conexion_bd import Sesion_dependencia
from sqlmodel import select

router = APIRouter(
    prefix="/transacciones",
    tags=["Transacciones"]
)

# ===================================
# CRUD TRANSACCIONES
# ===================================

@router.get("/")
async def listar_transacciones(session: Sesion_dependencia):
    # consulta = select(Transaccion)
    # lista_transacciones = session.exec(consulta).all()
    # return lista_transacciones
    return session.exec(select(Transaccion)).all()

@router.get("/{id}")
async def obtener_transaccion(id: int):
    pass


@router.post("/{factura_id}")
async def crear_transaccion(factura_id: int, datos_transaccion: TransaccionCrear, session : Sesion_dependencia):

    
    factura_encontrada = session.get(Factura, factura_id)

    

    if not factura_encontrada:

        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    #Validar datos de la transacción -json y pasamos a dict
    transaccion_dict = datos_transaccion.model_dump()
    transaccion_dict["factura_id"] = factura_id
    transaccion_val = Transaccion.model_validate(transaccion_dict)

    #Guardar en BD
    session.add(transaccion_val)
    session.commit()
    session.refresh(transaccion_val)
    return {
        "mensaje": "Transacción creada",
        "transaccion": transaccion_val
    }


@router.put("/transacciones/{id}")
async def editar_transaccion(
    id: int,
    datos_transaccion: TransaccionEditar
):

    for i, transaccion in enumerate(
        listas_transacciones
    ):

        if transaccion.id == id:

            transaccion_val = Transaccion.model_validate(
                datos_transaccion.model_dump()
            )

            transaccion_val.id = id
            transaccion_val.factura_id = (
                transaccion.factura_id
            )

            listas_transacciones[i] = transaccion_val

            return {
                "mensaje": "Transacción actualizada",
                "transaccion": transaccion_val
            }

    return {"error": "Transacción no encontrada"}


@router.delete("/transacciones/{id}")
async def eliminar_transaccion(id: int):

    for i, transaccion in enumerate(
        listas_transacciones
    ):

        if transaccion.id == id:

            del listas_transacciones[i]

            return {
                "mensaje": "Transacción eliminada"
            }

    return {"error": "Transacción no encontrada"}