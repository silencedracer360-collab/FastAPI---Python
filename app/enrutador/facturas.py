from fastapi import APIRouter, HTTPException, status
from app.model.factura import *
from ..conexion_bd import Sesion_dependencia
from sqlmodel import select


router = APIRouter(
    prefix="/facturas",
    tags=["Facturas"]
)


# ===================================
# CRUD FACTURAS
# ===================================

@router.get("/", response_model=list[FacturaLeerCompuesta])
async def listar_facturas(session: Sesion_dependencia):
    consulta = select(Factura)
    lista_facturas = session.exec(consulta).all()  
    return lista_facturas


@router.get("/{id}", response_model=FacturaLeerCompuesta)
async def obtener_factura(id: int, session: Sesion_dependencia):
    # Corrección: Busca directamente en la base de datos
    factura_bd = session.get(Factura, id)
    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"La factura con ID {id} no existe."
        )
    return factura_bd


@router.post("/{cliente_id}", response_model=Factura, status_code=status.HTTP_201_CREATED)
async def crear_factura(cliente_id: int, datos_factura: CrearFactura, session: Sesion_dependencia):
    cliente_encontrado = session.get(Cliente, cliente_id)
    if not cliente_encontrado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
        
    factura_dict = datos_factura.model_dump()
    factura_dict["cliente_id"] = cliente_id
    factura_val = Factura.model_validate(factura_dict)

    session.add(factura_val)
    session.commit()
    session.refresh(factura_val)
    return factura_val


@router.put("/{id}", response_model=Factura)
async def editar_factura(
    id: int,
    datos_factura: EditarFactura,
    session: Sesion_dependencia
):
    # Corrección: Trae el registro real de la base de datos
    factura_bd = session.get(Factura, id)
    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"La factura con ID {id} no existe."
        )

    # Reemplaza todos los datos (comportamiento PUT clásico)
    factura_dict = datos_factura.model_dump()
    factura_bd.sqlmodel_update(factura_dict)
    
    session.add(factura_bd)
    session.commit()
    session.refresh(factura_bd)
    return factura_bd


@router.delete("/{id}", response_model=Factura)
async def eliminar_factura(id: int, session: Sesion_dependencia):
    # Corrección: Elimina el registro físico de la base de datos
    factura_bd = session.get(Factura, id)
    if not factura_bd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"La factura con ID {id} no existe."
        )
        
    session.delete(factura_bd)
    session.commit()
    return factura_bd
