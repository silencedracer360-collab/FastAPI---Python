from pydantic import BaseModel, computed_field
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from app.model.cliente import Cliente
from app.model.transacciones import Transaccion


class FacturaBase(SQLModel):
    fecha: str = Field(default=datetime.now())
    # cliente: Cliente
    # transacciones: list[Transaccion] = []

    @computed_field
    @property
    def valor_total(self) -> float:
        return 0.0

class CrearFactura(FacturaBase):
    pass


class EditarFactura(FacturaBase):
    pass


class Factura(FacturaBase, table=True   ):
    id: int | None = Field(default=None, primary_key=True)
    cliente_id: int = Field(default=None, foreign_key="cliente.id")