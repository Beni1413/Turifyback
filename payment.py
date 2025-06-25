import mercadopago

sdk = mercadopago.SDK("TEST-790286877079251-062418-8244e69377e748f51bba3b14823bf7b8-2517892380")

def generar_preferencia(productos, pedido_numero, user_id, email, direccion):
    items = []
    for producto in productos:
        items.append({
            "title": producto["titulo"],
            "quantity": producto["cantidad"],
            "currency_id": "ARS",
            "unit_price": float(producto["precio_unitario"])
        })

    preference_data = {
        "items": items,
        "back_urls": {
            "success": "https://turify-deploy.web.app/success",
            "failure": "https://turify-deploy.web.app/failure",
            "pending": "https://turify-deploy.web.app/pending"
        },
        "auto_return": "approved",
        "metadata": {
            "pedido_numero": pedido_numero,
            "user_id": user_id,
            "email": email,
            "direccion": direccion,
            "productos": productos  # serializado completo
        }
    }

    preference = sdk.preference().create(preference_data)
    return preference["response"]["init_point"]

