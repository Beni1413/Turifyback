from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    surname = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=True, default="cliente")

    # Relación con el carrito
    cart_items = relationship("CartItem", back_populates="user")
    # Relación con pedidosPendientes
    pedidos = relationship("pedidosPendientes", back_populates="user")


class DetalleDePedido(Base):
    __tablename__ = "detalle_de_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos_pendientes.id"))
    servicio_id = Column(Integer, ForeignKey("servicios.id"))
    cantidad = Column(Integer, default=1)
    importe = Column(Integer, nullable=False)
    fecha_creacion = Column(String(50), nullable=False)

    # Relación inversa con pedidosPendientes
    pedido = relationship("pedidosPendientes", back_populates="detalles_pedido")
    # Relación inversa con Servicios
    servicio = relationship("Servicios", back_populates="detalles_pedido")


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("servicios.id"), nullable=False)
    cantidad = Column(Integer, default=1)
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relación inversa con User
    user = relationship("User", back_populates="cart_items")
    # Relación con Servicios
    servicio = relationship("Servicios", back_populates="cart_items")


class pedidosPendientes(Base):
    __tablename__ = "pedidos_pendientes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    servicio_id = Column(Integer, ForeignKey("servicios.id"), nullable=False)
    numero_pedido = Column(String(50), unique=True, nullable=False)
    monto_total = Column(Integer, nullable=False)
    estado = Column(String(20), default="pendiente")
    fecha_creacion = Column(String(50), nullable=False)
    direccion_entrega = Column(String(255), nullable=False)
    email_usuario = Column(String(100), nullable=False)

    # Relación inversa con User
    user = relationship("User", back_populates="pedidos")
    # Relación inversa con Servicios
    servicio = relationship("Servicios", back_populates="pedidos")
    # Relación con DetalleDePedido
    detalles_pedido = relationship("DetalleDePedido", back_populates="pedido")


class Servicios(Base):
    __tablename__ = "servicios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
    descripcion = Column(String(255), nullable=True)
    precio = Column(Integer, nullable=False)
    noches = Column(Integer, nullable=True)
    personas = Column(Integer, nullable=True)
    duracion = Column(Integer, nullable=True)
    clase = Column(String(50), nullable=True)
    dias = Column(String(50), nullable=True)
    gama = Column(String(50), nullable=True)
     # Relación inversa con pedidosPendientes
    pedidos = relationship("pedidosPendientes", back_populates="servicio")
    # Relación con el carrito
    cart_items = relationship("CartItem", back_populates="servicio")
    # Relación con DetalleDePedido
    detalles_pedido = relationship("DetalleDePedido", back_populates="servicio")


