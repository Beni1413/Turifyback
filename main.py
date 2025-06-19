from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
import models, schemas, database, crud
from fastapi import APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from database import get_db
from schemas import DetalleDePedidoCreate, DetalleDePedidoOut
from typing import List
from schemas import ServicioCreate, ServicioOut
from typing import List
import crud, schemas
from schemas import PedidoEstadoUpdate
from fastapi import Body
from fastapi import HTTPException
from schemas import ServicioUpdate

app = FastAPI()

origins = [
    "http://localhost:4200"
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
    return {"message": "Login exitoso", "user_id": db_user.id, "role": db_user.rol, "name": db_user.name}

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

@app.post("/pedidos/", response_model=schemas.PedidoCabecera)
def create_pedido(
    pedido: schemas.PedidoCabeceraCreate,
    db: Session = Depends(get_db)
):
    return crud.create_pedido(db, pedido)
@app.post("/pedidos/detalle", response_model=List[DetalleDePedidoOut])
def crear_detalle(detalles: List[DetalleDePedidoCreate], db: Session = Depends(get_db)):
    return crud.crear_detalle_de_pedido(db, detalles)

@app.put("/pedidos/estado")
def cambiar_estado_pedido(update: PedidoEstadoUpdate, db: Session = Depends(get_db)):
    pedido_actualizado = crud.actualizar_estado_pedido(db, update.id, update.nuevo_estado)
    if not pedido_actualizado:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return {"msg": "Estado actualizado correctamente", "nuevo_estado": pedido_actualizado.estado}

@app.post("/servicios/", response_model=ServicioOut)
def crear_servicio(servicio: ServicioCreate, db: Session = Depends(get_db)):
    return crud.crear_servicio(db, servicio.id, servicio.nombre, servicio.descripcion, servicio.precio, servicio.categoria)

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

