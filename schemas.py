from pydantic import BaseModel
from datetime import date
from typing import List

class UserCreate(BaseModel):
    name: str
    surname: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class CartItemBase(BaseModel):
    product_id: int
    quantity: int

class CartItemCreate(CartItemBase):
    user_id: int

class CartItemUpdate(BaseModel):
    product_id: int
    quantity: int

class CartItemOut(CartItemBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class PedidoCabeceraCreate(BaseModel):
    user_id: int
    servicio_id: int
    numero_pedido: str
    monto_total: float
    estado: str = "pendiente"
    fecha_creacion: date
    direccion_entrega: str
    email_usuario: str

    class Config:
        from_attributes = True 

class PedidoCabecera(PedidoCabeceraCreate):
    id: int

    class Config:
        orm_mode = True
class DetalleDePedidoCreate(BaseModel):
    pedido_id: int
    servicio_id: int
    cantidad: int
    importe: float
    fecha_creacion: str

    class Config:
        orm_mode = True

class DetalleDePedidoOut(DetalleDePedidoCreate):
    id: int

class PedidoEstadoUpdate(BaseModel):
    id: int
    nuevo_estado: str

class ServicioCreate(BaseModel):
    nombre: str
    categoria: str
    descripcion: str = None
    precio: int
    noches: int = None
    personas: int = None
    duracion: int = None
    clase: str = None
    dias: str = None
    gama: str = None

    class Config:
        orm_mode = True

class ServicioOut(ServicioCreate):
    id: int

class ServicioOut(BaseModel):
    id: int
    nombre: str
    categoria: str
    descripcion: str = None
    precio: int
    noches: int = None
    personas: int = None
    duracion: int = None
    clase: str = None
    dias: str = None
    gama: str = None

    class Config:
        orm_mode = True

class ServicioOut(BaseModel):
    id: int
    nombre: str
    categoria: str
    descripcion: str | None = None
    precio: int
    noches: int | None = None
    personas: int | None = None
    duracion: int | None = None
    clase: str | None = None
    dias: str | None = None
    gama: str | None = None

    class Config:
        from_attributes = True
