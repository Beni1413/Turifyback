from sqlalchemy.orm import Session
from models import User, CartItem, pedidosPendientes, DetalleDePedido, Servicios
from schemas import UserCreate, CartItemCreate, PedidoCabeceraCreate, DetalleDePedidoCreate, ServicioCreate, ServicioUpdate
from passlib.context import CryptContext
from datetime import datetime
from emails import enviar_mail_confirmacion

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

def procesar_pedido_completo(db: Session, pedido_data: PedidoCabeceraCreate, detalles_data: list[DetalleDePedidoCreate]):
    db_pedido = pedidosPendientes(
        user_id=pedido_data.user_id,
        servicio_id=pedido_data.servicio_id,
        numero_pedido=pedido_data.numero_pedido,
        monto_total=pedido_data.monto_total,
        estado=pedido_data.estado,
        fecha_creacion=pedido_data.fecha_creacion or datetime.utcnow(),
        direccion_entrega=pedido_data.direccion_entrega,
        email_usuario=pedido_data.email_usuario
    )
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido


def actualizar_estado_pedido(db: Session, pedido_id: int, nuevo_estado: str):
    pedido = db.query(pedidosPendientes).filter(pedidosPendientes.id == pedido_id).first()
    if not pedido:
        return None
    pedido.estado = nuevo_estado
    db.commit()
    db.refresh(pedido)
    return pedido

def anular_pedido(db: Session, pedido_id: int):
    pedido = db.query(pedidosPendientes).filter(pedidosPendientes.id == pedido_id).first()
    if not pedido or pedido.estado == "anulado":
        return pedido
    pedido.estado = "anulado"
    db.commit()
    db.refresh(pedido)
    return pedido

def get_pedidos_por_usuario(db: Session, user_id: int):
    return db.query(pedidosPendientes).filter(pedidosPendientes.user_id == user_id).all()

def get_pedidos_con_servicio(db: Session, user_id: int):
    return (
        db.query(
            pedidosPendientes.id,
            pedidosPendientes.numero_pedido,
            pedidosPendientes.monto_total,
            pedidosPendientes.estado,
            pedidosPendientes.fecha_creacion,
            pedidosPendientes.direccion_entrega,
            pedidosPendientes.email_usuario,
            Servicios.id.label("servicio_id"),
            Servicios.nombre.label("nombre_servicio"),
            Servicios.categoria.label("categoria_servicio")
        )
        .join(Servicios, pedidosPendientes.servicio_id == Servicios.id)
        .filter(pedidosPendientes.user_id == user_id)
        .all()
    )

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

def get_all_pedidos(db: Session):
    return (
        db.query(
            pedidosPendientes.id,
            pedidosPendientes.numero_pedido,
            pedidosPendientes.monto_total,
            pedidosPendientes.estado,
            pedidosPendientes.fecha_creacion,
            pedidosPendientes.direccion_entrega,
            pedidosPendientes.email_usuario,
            Servicios.id.label("servicio_id"),
            Servicios.nombre.label("nombre_servicio"),
            Servicios.categoria.label("categoria_servicio")
        )
        .join(Servicios, pedidosPendientes.servicio_id == Servicios.id)
        .order_by(pedidosPendientes.fecha_creacion.desc())
        .all()
    )

def eliminar_pedido(db: Session, pedido_id: int):
    pedido = db.query(pedidosPendientes).filter(pedidosPendientes.id == pedido_id).first()
    if not pedido:
        return False
    db.delete(pedido)
    db.commit()
    return True

def crear_detalle_de_pedido(db: Session, detalles: list[DetalleDePedidoCreate]):
    nuevos_detalles = []
    for detalle_data in detalles:
        nuevo = DetalleDePedido(**detalle_data.dict())
        db.add(nuevo)
        nuevos_detalles.append(nuevo)
    db.commit()
    for d in nuevos_detalles:
        db.refresh(d)

    if not nuevos_detalles:
        return []

    pedido_id = nuevos_detalles[0].pedido_id
    pedido = db.query(pedidosPendientes).get(pedido_id)
    if not pedido:
        return nuevos_detalles

    usuario = db.query(User).get(pedido.user_id)

    lista_detalles = []
    for d in nuevos_detalles:
        servicio = db.query(Servicios).get(d.servicio_id)
        if servicio:
            lista_detalles.append({
                "nombre": servicio.nombre,
                "categoria": servicio.categoria,
                "precio": servicio.precio,
                "cantidad": d.cantidad
            })

    if lista_detalles:
        enviar_mail_confirmacion(
            destinatario=pedido.email_usuario,
            nombre=usuario.name if usuario else "Cliente",
            numero_pedido=pedido.numero_pedido,
            detalles=lista_detalles,
            direccion=pedido.direccion_entrega,
            fecha=pedido.fecha_creacion.strftime("%d/%m/%Y")
        )

    return nuevos_detalles



