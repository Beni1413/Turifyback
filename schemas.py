from pydantic import BaseModel
from datetime import date
from typing import List
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str
    surname: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    rol: str  # si tenés roles

    class Config:
        from_attributes = True

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
    fecha_creacion: datetime
    direccion_entrega: str
    email_usuario: str

    class Config:
        from_attributes = True 

class PedidoCabeceraSimple(PedidoCabeceraCreate):
    id: int

    class Config:
        orm_mode = True

class PedidoCabeceraConServicios(BaseModel):
    id: int
    numero_pedido: str
    monto_total: float
    estado: str
    fecha_creacion: datetime
    direccion_entrega: str
    email_usuario: str
    servicio_id: int
    nombre_servicio: str
    categoria_servicio: str

    class Config:
        from_attributes = True

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

class PedidoAnulacion(BaseModel):
    pedido_id: int

    class Config:
        from_attributes = True

class ServicioCreate(BaseModel):
    nombre: str
    categoria: str
    descripcion: str 
    precio: float
    noches: Optional[int] = None
    personas: Optional[int] = None
    duracion: Optional[str] = None
    clase: Optional[str] = None
    dias: Optional[int] = None
    gama: Optional[str] = None

    class Config:
        orm_mode = True

class ServicioOut(ServicioCreate):
    id: int

class ServicioOut(BaseModel):
    id: int
    nombre: str
    categoria: str
    descripcion: Optional[str] = None
    precio: int
    noches: Optional[int] = None
    personas: Optional[int] = None
    duracion: Optional[str] = None
    clase: Optional[str] = None
    dias: Optional[str] = None
    gama: Optional[str] = None

    class Config:
        from_attributes = True 

class ServicioUpdate(BaseModel):
    nombre: str | None = None
    categoria: str | None = None
    descripcion: str | None = None
    precio: int | None = None
    noches: int | None = None
    personas: int | None = None
    duracion: str | None = None
    clase: str | None = None
    dias: str | None = None
    gama: str | None = None

    class Config:
        from_attributes = True

