import mercadopago

sdk = mercadopago.SDK("TEST-3063286480776161-062415-9fd686a7c377b8457b74af32663c8482-1343558942")

def generar_preferencia(servicio, cantidad, precio_unitario, pedido_numero: str):
    data = {
        "items": [{
            "title": servicio,
            "quantity": cantidad,
            "unit_price": precio_unitario
        }],
        "back_urls": {
            "success": "https://turify-deploy.web.app/success",
            "failure": "https://turify-deploy.web.app/failure",
            "pending": "https://turify-deploy.web.app/pending"
        },
        "auto_return": "approved",
        "metadata": {
            "pedido_numero": pedido_numero
        }
    }

    res = sdk.preference().create(data)
    return res["response"]["init_point"]

