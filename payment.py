import mercadopago

sdk = mercadopago.SDK("TEST-6297043000243115-062416-be6247174c0882f0f279d1827c2de9b8-1302080610")

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

