from pydantic import BaseModel, computed_field
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from app.model.cliente import Cliente, ClienteLeer
from app.model.transacciones import Transaccion


class FacturaBase(SQLModel):
    fecha: str = Field(default=datetime.now())



class CrearFactura(FacturaBase):
    pass


class EditarFactura(FacturaBase):
    pass


class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    cliente_id: int = Field(default=None, foreign_key="cliente.id")
    #Crear relaciones virtuales CLiente, Transacciones - No en la BD
    cliente : Cliente = Relationship(back_populates="factura")
    transacciones : list[Transaccion] = Relationship(back_populates="factura")

    @computed_field
    @property
    def valor_total(self) -> float:
        total_factura = 0.0
        if self.transacciones == None:
            return total_factura
        for transaccion in self.transacciones:
            total_factura += transaccion.vr_unitario * transaccion.cantidad
        return total_factura

    
#Modelo para mostrar al CLiente o Usuario
class FacturaLeer(FacturaBase):
    id : int
    cliente : ClienteLeer
    valor_total : float
    
class FacturaLeerCompuesta(FacturaLeer):
    transacciones : list[Transaccion] = []

        
