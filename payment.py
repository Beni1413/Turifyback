import mercadopago

sdk = mercadopago.SDK("TEST-790286877079251-062418-8244e69377e748f51bba3b14823bf7b8-2517892380")

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

