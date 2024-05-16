from pydantic import BaseModel
from datetime import date, time, datetime

class usuarios(BaseModel):
    usuario: str
    cc:int
    email:str
    contraseña: str
    telefono:str
    Rol:str

class pedidos(BaseModel):
    Fecha_pedido:datetime
    Estado: str

class detalle_pedidos(BaseModel):
    Cantidad:int
    Precio_unitario: float

class productos(BaseModel):
    Nombre_producto: str
    Referencia:str
    precio:float
    Categoria: str
    Stock_disponible:int

class pagos(BaseModel):
    Fecha_pago: datetime
    Detalle_pago:str
    Forma_pago:str
    Total_pago: float
  
class facturacion(BaseModel):
   Fecha_factura:datetime
   Total_facturado:float