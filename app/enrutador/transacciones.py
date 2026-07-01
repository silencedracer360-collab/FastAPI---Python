from fastapi import APIRouter, HTTPException, status
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

@router.get("/", response_model=list[Transaccion])
async def listar_transacciones(session: Sesion_dependencia):
    return session.exec(select(Transaccion)).all()


@router.get("/{id}", response_model=Transaccion)
async def obtener_transaccion(id: int, session: Sesion_dependencia):
    # Conectado a la base de datos
    transaccion_bd = session.get(Transaccion, id)
    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La transacción con ID {id} no existe."
        )
    return transaccion_bd


@router.post("/{factura_id}", response_model=Transaccion, status_code=status.HTTP_201_CREATED)
async def crear_transaccion(factura_id: int, datos_transaccion: TransaccionCrear, session: Sesion_dependencia):
    factura_encontrada = session.get(Factura, factura_id)
    if not factura_encontrada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Factura no encontrada"
        )

    transaccion_dict = datos_transaccion.model_dump()
    transaccion_dict["factura_id"] = factura_id
    transaccion_val = Transaccion.model_validate(transaccion_dict)

    session.add(transaccion_val)
    session.commit()
    session.refresh(transaccion_val)
    return transaccion_val


@router.put("/{id}", response_model=Transaccion)
async def editar_transaccion(
    id: int,
    datos_transaccion: TransaccionEditar,
    session: Sesion_dependencia
):
    # Busca el registro real en la base de datos
    transaccion_bd = session.get(Transaccion, id)
    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La transacción con ID {id} no existe."
        )

    # Convierte los datos de entrada a diccionario
    transaccion_dict = datos_transaccion.model_dump()
    
    # Mantiene el mismo factura_id original si el esquema de edición no lo incluye
    transaccion_bd.sqlmodel_update(transaccion_dict)
    
    session.add(transaccion_bd)
    session.commit()
    session.refresh(transaccion_bd)
    return transaccion_bd


@router.delete("/{id}", response_model=Transaccion)
async def eliminar_transaccion(id: int, session: Sesion_dependencia):
    # Busca y elimina físicamente de la base de datos
    transaccion_bd = session.get(Transaccion, id)
    if not transaccion_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La transacción con ID {id} no existe."
        )
        
    session.delete(transaccion_bd)
    session.commit()
    return transaccion_bd