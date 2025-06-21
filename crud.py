from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
from passlib.context import CryptContext
from models import CartItem
from schemas import CartItemCreate
from schemas import PedidoCabeceraCreate
from models import DetalleDePedido
from schemas import DetalleDePedidoCreate
from models import Servicios
from schemas import ServicioCreate
from models import pedidosPendientes
from models import Servicios
from schemas import ServicioUpdate
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        name=user.name,
        surname=user.surname,
        email=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_cart(db: Session, user_id: int):
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()

def add_item(db: Session, item: CartItemCreate):
    db_item = CartItem(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def remove_item(db: Session, user_id: int, product_id: int):
    item = db.query(CartItem).filter(CartItem.user_id == user_id, CartItem.product_id == product_id).first()
    if item:
        db.delete(item)
        db.commit()

def create_pedido(db: Session, pedido: PedidoCabeceraCreate):
    db_pedido = pedidosPendientes(
        user_id=pedido.user_id,
        servicio_id=pedido.servicio_id,
        numero_pedido=pedido.numero_pedido,
        monto_total=pedido.monto_total,
        estado=pedido.estado,
        fecha_creacion=pedido.fecha_creacion or datetime.utcnow(),  
        direccion_entrega=pedido.direccion_entrega,
        email_usuario=pedido.email_usuario
    )
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

def crear_detalle_de_pedido(db: Session, detalles: list[DetalleDePedidoCreate]):
    nuevos_detalles = []
    for detalle_data in detalles:
        nuevo = detalleDePedido(**detalle_data.dict())
        db.add(nuevo)
        nuevos_detalles.append(nuevo)
    db.commit()
    for d in nuevos_detalles:
        db.refresh(d)
    return nuevos_detalles

def actualizar_estado_pedido(db: Session, pedido_id: int, nuevo_estado: str):
    pedido = db.query(pedidosPendientes).filter(pedidosPendientes.id == pedido_id).first()
    if not pedido:
        return None
    pedido.estado = nuevo_estado
    db.commit()
    db.refresh(pedido)
    return pedido

def crear_servicio(db: Session, servicio: ServicioCreate):
    nuevo_servicio = Servicios(**servicio.dict())
    db.add(nuevo_servicio)
    db.commit()
    db.refresh(nuevo_servicio)
    return nuevo_servicio
    
def filtrar_servicios_por_categoria(db: Session, categoria: str):
    return db.query(Servicios).filter(Servicios.categoria == categoria).all()

def get_all_servicios(db: Session):
    return db.query(Servicios).all()

def actualizar_servicio(db: Session, servicio_id: int, datos: ServicioUpdate):
    servicio = db.query(Servicios).filter(Servicios.id == servicio_id).first()
    if not servicio:
        return None

    for campo, valor in datos.dict(exclude_unset=True).items():
        setattr(servicio, campo, valor)

    db.commit()
    db.refresh(servicio)
    return servicio

def eliminar_servicio(db: Session, servicio_id: int):
    servicio = db.query(Servicios).filter(Servicios.id == servicio_id).first()
    if not servicio:
        return False
    db.delete(servicio)
    db.commit()
    return True
