from fastapi import APIRouter, HTTPException
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

@router.get("/", response_model=list[FacturaLeer])
async def listar_facturas(session : Sesion_dependencia):
    # select * from facturas
    consulta = select(Factura)
    lista_facturas = session.exec(consulta).all()  
    return lista_facturas


@router.get("/{id}")
async def obtener_factura(id: int):

    for factura in listas_facturas:

        if factura.id == id:
            return factura

    return {"error": "Factura no encontrada"}


@router.post("/{cliente_id}")
async def crear_factura(cliente_id: int, datos_factura: CrearFactura, session: Sesion_dependencia):

    cliente_encontrado = session.get(Cliente, cliente_id)
    if not cliente_encontrado:

        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    #validar datos de la fatura-json, pasar dict
    factura_dict = datos_factura.model_dump()
    factura_dict["cliente_id"] = cliente_id
    factura_val = Factura.model_validate(factura_dict)

    #guardar en bd
    session.add(factura_val)
    session.commit()
    session.refresh(factura_val)
    return factura_val


@router.put("/{id}")
async def editar_factura(
    id: int,
    datos_factura: EditarFactura
):

    for i, factura in enumerate(listas_facturas):

        if factura.id == id:

            factura_val = Factura.model_validate(
                datos_factura.model_dump()
            )

            factura_val.id = id

            listas_facturas[i] = factura_val

            return {
                "mensaje": "Factura actualizada",
                "factura": factura_val
            }

    return {"error": "Factura no encontrada"}


@router.delete("/{id}")
async def eliminar_factura(id: int):

    for i, factura in enumerate(listas_facturas):

        if factura.id == id:

            del listas_facturas[i]

            return {
                "mensaje": "Factura eliminada"
            }

    return {"error": "Factura no encontrada"}
