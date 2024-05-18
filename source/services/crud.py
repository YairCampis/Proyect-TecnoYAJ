from pydantic import BaseModel
from source.database import db_mysql
from source.models import models
from sqlalchemy.orm import Session



# Funciones CRUD para la tabla de usuarios
def crear_usuario(usuario):
    cursor = db_mysql.cursor()
    query = "INSERT INTO usuarios (usuario, cc, email, contraseña, telefono, Rol) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (usuario.usuario, usuario.cc, usuario.email, usuario.contraseña, usuario.telefono, usuario.Rol))
    db_mysql.commit()
    return usuario


def get_user(db: Session, usuario: str):
    return db.query(BaseModel).filter(BaseModel.usuario == usuario).first()

def obtener_usuario_por_id(user_id):
    cursor = db_mysql.cursor(dictionary=True)
    query = "SELECT * FROM usuarios WHERE id = %s"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()

def actualizar_usuario(user_id, usuario_actualizado):
    cursor = db_mysql.cursor()
    query = "UPDATE usuarios SET usuario = %s, cc = %s, email = %s, contraseña = %s, telefono = %s, Rol = %s WHERE id = %s"
    cursor.execute(query, (usuario_actualizado.usuario, usuario_actualizado.cc, usuario_actualizado.email, usuario_actualizado.contraseña, usuario_actualizado.telefono, usuario_actualizado.Rol, user_id))
    db_mysql.commit()

def eliminar_usuario(user_id):
    cursor = db_mysql.cursor()
    query = "DELETE FROM usuarios WHERE id = %s"
    cursor.execute(query, (user_id,))
    db_mysql.commit()

# Funciones CRUD para la tabla de pedidos
def crear_pedido(pedido):
    cursor = db_mysql.cursor()
    query = "INSERT INTO pedidos (Fecha_pedido, Estado) VALUES (%s, %s)"
    cursor.execute(query, (pedido.Fecha_pedido, pedido.Estado))
    db_mysql.commit()
    return pedido

def obtener_pedido_por_id(order_id):
    cursor = db_mysql.cursor(dictionary=True)
    query = "SELECT * FROM pedidos WHERE id = %s"
    cursor.execute(query, (order_id,))
    return cursor.fetchone()

def actualizar_pedido(order_id, pedido_actualizado):
    cursor = db_mysql.cursor()
    query = "UPDATE pedidos SET Fecha_pedido = %s, Estado = %s WHERE id = %s"
    cursor.execute(query, (pedido_actualizado.Fecha_pedido, pedido_actualizado.Estado, order_id))
    db_mysql.commit()

def eliminar_pedido(order_id):
    cursor = db_mysql.cursor()
    query = "DELETE FROM pedidos WHERE id = %s"
    cursor.execute(query, (order_id,))
    db_mysql.commit()


    # Funciones CRUD para la tabla de detalle de pedidos
def crear_detalle_pedido(detalle_pedido):
    cursor = db_mysql.cursor()
    query = "INSERT INTO detalle_pedidos (Cantidad, Precio_unitario) VALUES (%s, %s)"
    cursor.execute(query, (detalle_pedido.Cantidad, detalle_pedido.Precio_unitario))
    db_mysql.commit()
    return detalle_pedido

def obtener_detalle_pedido_por_id(order_detail_id):
    cursor = db_mysql.cursor(dictionary=True)
    query = "SELECT * FROM detalle_pedidos WHERE id = %s"
    cursor.execute(query, (order_detail_id,))
    return cursor.fetchone()

def actualizar_detalle_pedido(order_detail_id, detalle_pedido_actualizado):
    cursor = db_mysql.cursor()
    query = "UPDATE detalle_pedidos SET Cantidad = %s, Precio_unitario = %s WHERE id = %s"
    cursor.execute(query, (detalle_pedido_actualizado.Cantidad, detalle_pedido_actualizado.Precio_unitario, order_detail_id))
    db_mysql.commit()

def eliminar_detalle_pedido(order_detail_id):
    cursor = db_mysql.cursor()
    query = "DELETE FROM detalle_pedidos WHERE id = %s"
    cursor.execute(query, (order_detail_id,))
    db_mysql.commit()

    # Funciones CRUD para la tabla de productos
def crear_producto(producto):
    cursor = db_mysql.cursor()
    query = "INSERT INTO productos (Nombre_producto, Referencia, precio, Categoria, Stock_disponible) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (producto.Nombre_producto, producto.Referencia, producto.precio, producto.Categoria, producto.Stock_disponible))
    db_mysql.commit()
    return producto

def obtener_producto_por_id(product_id):
    cursor = db_mysql.cursor(dictionary=True)
    query = "SELECT * FROM productos WHERE id = %s"
    cursor.execute(query, (product_id,))
    return cursor.fetchone()

def actualizar_producto(product_id, producto_actualizado):
    cursor = db_mysql.cursor()
    query = "UPDATE productos SET Nombre_producto = %s, Referencia = %s, precio = %s, Categoria = %s, Stock_disponible = %s WHERE id = %s"
    cursor.execute(query, (producto_actualizado.Nombre_producto, producto_actualizado.Referencia, producto_actualizado.precio, producto_actualizado.Categoria, producto_actualizado.Stock_disponible, product_id))
    db_mysql.commit()

def eliminar_producto(product_id):
    cursor = db_mysql.cursor()
    query = "DELETE FROM productos WHERE id = %s"
    cursor.execute(query, (product_id,))
    db_mysql.commit()

    # Funciones CRUD para la tabla de pagos
def crear_pago(pago):
    cursor = db_mysql.cursor()
    query = "INSERT INTO pagos (Fecha_pago, Detalle_pago, Forma_pago, Total_pago) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (pago.Fecha_pago, pago.Detalle_pago, pago.Forma_pago, pago.Total_pago))
    db_mysql.commit()
    return pago

def obtener_pago_por_id(payment_id):
    cursor = db_mysql.cursor(dictionary=True)
    query = "SELECT * FROM pagos WHERE id = %s"
    cursor.execute(query, (payment_id,))
    return cursor.fetchone()

def actualizar_pago(payment_id, pago_actualizado):
    cursor = db_mysql.cursor()
    query = "UPDATE pagos SET Fecha_pago = %s, Detalle_pago = %s, Forma_pago = %s, Total_pago = %s WHERE id = %s"
    cursor.execute(query, (pago_actualizado.Fecha_pago, pago_actualizado.Detalle_pago, pago_actualizado.Forma_pago, pago_actualizado.Total_pago, payment_id))
    db_mysql.commit()

def eliminar_pago(payment_id):
    cursor = db_mysql.cursor()
    query = "DELETE FROM pagos WHERE id = %s"
    cursor.execute(query, (payment_id,))
    db_mysql.commit()

    # Funciones CRUD para la tabla de facturación
def crear_factura(factura):
    cursor = db_mysql.cursor()
    query = "INSERT INTO facturacion (Fecha_factura, Total_facturado) VALUES (%s, %s)"
    cursor.execute(query, (factura.Fecha_factura, factura.Total_facturado))
    db_mysql.commit()
    return factura

def obtener_factura_por_id(invoice_id):
    cursor = db_mysql.cursor(dictionary=True)
    query = "SELECT * FROM facturacion WHERE id = %s"
    cursor.execute(query, (invoice_id,))
    return cursor.fetchone()

def actualizar_factura(invoice_id, factura_actualizada):
    cursor = db_mysql.cursor()
    query = "UPDATE facturacion SET Fecha_factura = %s, Total_facturado = %s WHERE id = %s"
    cursor.execute(query, (factura_actualizada.Fecha_factura, factura_actualizada.Total_facturado, invoice_id))
    db_mysql.commit()

def eliminar_factura(invoice_id):
    cursor = db_mysql.cursor()
    query = "DELETE FROM facturacion WHERE id = %s"
    cursor.execute(query, (invoice_id,))
    db_mysql.commit()