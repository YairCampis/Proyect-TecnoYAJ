
from fastapi import FastAPI
from source.services.crud import crear_detalle_pedido
from source.services.schemas import detalle_pedidos


app = FastAPI()

@app.post("/detalle_pedidos/", response_model=detalle_pedidos)
async def crear_detalle_pedidos(detped:detalle_pedidos):
   return crear_detalle_pedido(detped)