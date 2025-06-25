from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from database import get_db
from schemas import DetalleDePedidoCreate, DetalleDePedidoOut
from typing import List
from schemas import ServicioCreate, ServicioOut
from typing import List
from schemas import PedidoEstadoUpdate
from fastapi import Body
from fastapi import HTTPException
from schemas import ServicioUpdate
import crud, schemas
import models, schemas, database, crud
from dependencies import verificar_admin
from fastapi import Depends
from dependencies import get_current_user  # si tenés esto
from models import User 
from payment import generar_preferencia
from schemas import Pago

app = FastAPI()

origins = [
    "https://turify-deploy.web.app",
    "https://turify-deploy.firebaseapp.com"
]
# Crea tablas en la base de datos
models.Base.metadata.create_all(bind=database.engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Orígenes permitidos
    allow_credentials=True,           # Permitir cookies/autenticación
    allow_methods=["*"],              # Métodos HTTP permitidos
    allow_headers=["*"],              # Headers permitidos
)
# Dependencia para obtener sesión DB
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verificar si ya existe el email
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Este mail ya está registrado")

    # Crear nuevo usuario
    nuevo_usuario = models.User(
        name=user.name,
        surname=user.surname,
        email=user.email,
        password=user.password 
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return {"message": "Usuario creado correctamente", "user_id": nuevo_usuario.id}

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(
        models.User.email == user.email,
        models.User.password == user.password
    ).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return {"message": "Login exitoso", "user_id": db_user.id, "role": db_user.rol, "name": db_user.name, "email": db_user.email, "surname": db_user.surname}

@app.get("/usuarios/{user_id}", response_model=schemas.UserOut)
def obtener_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = crud.get_user_by_id(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.get("/clientes", response_model=List[schemas.UserOut])
def listar_clientes(db: Session = Depends(get_db)):
    return crud.get_all_clientes(db)

@app.get("/cart/{user_id}", response_model=list[schemas.CartItemOut])
def get_cart(user_id: int, db: Session = Depends(get_db)):
    return crud.get_cart(db, user_id)

@app.post("/cart/add", response_model=schemas.CartItemOut)
def add_to_cart(item: schemas.CartItemCreate, db: Session = Depends(get_db)):
    return crud.add_item(db, item)

@app.post("/cart/remove")
def remove_from_cart(user_id: int, product_id: int, db: Session = Depends(get_db)):
    crud.remove_item(db, user_id, product_id)
    return {"msg": "Se eliminó el producto del carrito"}

@app.post("/pedidos/", response_model=schemas.PedidoCabeceraSimple)
def create_pedido(pedido: schemas.PedidoCabeceraCreate, db: Session = Depends(get_db)):
    return crud.procesar_pedido_completo(db, pedido_data=pedido, detalles_data=[])

@app.post("/pedidos/detalle", response_model=List[DetalleDePedidoOut])
def crear_detalle(detalles: List[DetalleDePedidoCreate], db: Session = Depends(get_db)):
    return crud.crear_detalle_de_pedido(db, detalles)

@app.put("/pedidos/estado")
def cambiar_estado_pedido(update: PedidoEstadoUpdate, db: Session = Depends(get_db)):
    pedido_actualizado = crud.actualizar_estado_pedido(db, update.id, update.nuevo_estado)
    if not pedido_actualizado:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"msg": "Estado actualizado correctamente", "nuevo_estado": pedido_actualizado.estado}

@app.get("/pedidos/", response_model=List[schemas.PedidoCabeceraConServicios])
def obtener_pedidos(db: Session = Depends(get_db)):
    return crud.get_all_pedidos(db)

@app.put("/pedidos/anular")
def anular_pedido(data: schemas.PedidoAnulacion, db: Session = Depends(get_db)):
    pedido = crud.anular_pedido(db, data.pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"mensaje": "Pedido anulado correctamente", "estado": pedido.estado}

@app.get("/pedidos/mios", response_model=List[schemas.PedidoCabeceraConServicios])
def obtener_mis_pedidos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud.get_pedidos_con_servicio(db, current_user.id)

@app.delete("/pedidos/{pedido_id}")
def eliminar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    exito = crud.eliminar_pedido(db, pedido_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"mensaje": "Pedido eliminado correctamente"}


@app.post("/servicios/", response_model=ServicioOut)
def crear_servicio(servicio: ServicioCreate, db: Session = Depends(get_db)):
    return crud.crear_servicio(db, servicio)


@app.get("/servicios/filtrar", response_model=List[schemas.ServicioOut])
def filtrar_por_categoria(categoria: str, db: Session = Depends(get_db)):
    servicios = crud.filtrar_servicios_por_categoria(db, categoria)
    if not servicios:
        raise HTTPException(status_code=404, detail="No se encontraron servicios con esa categoría")
    return servicios

@app.get("/servicios/", response_model=list[schemas.ServicioOut])
def listar_servicios(db: Session = Depends(get_db)):
    return crud.get_all_servicios(db)

@app.put("/servicios/{servicio_id}", response_model=schemas.ServicioOut)
def update_servicio(servicio_id: int, data: schemas.ServicioUpdate, db: Session = Depends(get_db)):
    servicio_actualizado = crud.actualizar_servicio(db, servicio_id, data)
    if not servicio_actualizado:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio_actualizado

@app.delete("/servicios/{servicio_id}")
def borrar_servicio(servicio_id: int, db: Session = Depends(get_db)):
    exito = crud.eliminar_servicio(db, servicio_id)
    if not exito:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return {"mensaje": "Servicio eliminado correctamente"}

@app.get("/admin/dashboard")
def admin_dashboard(_ = Depends(verificar_admin)):
    return {"msg": "Bienvenido Admin"}

@app.post("/pago")
def crear_pago(pago: Pago):
    url = generar_preferencia(
        productos=[item.dict() for item in pago.productos],
        pedido_numero=pago.pedido_numero,
        user_id=pago.user_id,
        email=pago.email,
        direccion=pago.direccion
    )
    return {"init_point": url}


@app.post("/webhook")
def recibir_webhook(payload: dict = Body(...), db: Session = Depends(get_db)):
    if payload.get("type") == "payment":
        payment_id = payload["data"]["id"]

        try:
            payment_info = sdk.payment().get(payment_id)
            status = payment_info["response"]["status"]
            metadata = payment_info["response"].get("metadata", {})
        except Exception as e:
            return {"status": "error", "detail": str(e)}

        if status == "approved":
            pedido_numero = metadata.get("pedido_numero")
            user_id = metadata.get("user_id")
            email = metadata.get("email")
            direccion = metadata.get("direccion")
            productos = metadata.get("productos", [])

            # Solo guardar si no está guardado aún
            existente = db.query(pedidosPendientes).filter_by(numero_pedido=pedido_numero).first()
            if not existente:
                monto_total = sum(p["cantidad"] * p["precio_unitario"] for p in productos)

                pedido = pedidosPendientes(
                    numero_pedido=pedido_numero,
                    user_id=user_id,
                    monto_total=monto_total,
                    estado="pendiente",
                    fecha_creacion=datetime.utcnow(),
                    direccion_entrega=direccion,
                    email_usuario=email
                )
                db.add(pedido)
                db.commit()
                db.refresh(pedido)

                for producto in productos:
                    detalle = PedidoDetalle(
                        pedido_id=pedido.id,
                        servicio_id=producto["servicio_id"],
                        cantidad=producto["cantidad"],
                        importe=producto["cantidad"] * producto["precio_unitario"]
                    )
                    db.add(detalle)

                db.commit()

                # Enviar mail de confirmación
                usuario = db.query(User).get(user_id)
                enviar_mail_pago_confirmado(
                    destinatarios=[email, "turifycontacto@gmail.com"],
                    nombre=usuario.name if usuario else "Cliente",
                    numero_pedido=pedido_numero,
                    monto=monto_total,
                    fecha=datetime.utcnow().strftime("%d/%m/%Y")
                )

                return {"status": "pedido_guardado"}

    return {"status": "sin_accion"}