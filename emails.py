import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def generar_html_confirmacion(nombre, numero_pedido, detalles, direccion, fecha):
    subtotal = sum(d["cantidad"] * d["precio"] for d in detalles)
    iva = round(subtotal * 0.21, 2)
    total = round(subtotal + iva, 2)

    filas = ""
    for item in detalles:
        filas += f"""
        <tr>
            <td>{item['nombre']}</td>
            <td>{item['categoria']}</td>
            <td>{item['cantidad']}</td>
            <td>${item['precio']}</td>
            <td>${item['cantidad'] * item['precio']}</td>
        </tr>
        """

    html = f"""\
    <html>
      <head>
        <style>
          table {{
            width: 100%;
            border-collapse: collapse;
          }}
          th, td {{
            border: 1px solid #ddd;
            padding: 8px;
          }}
          th {{
            background-color: #f2f2f2;
          }}
          .totales {{
            margin-top: 20px;
            font-weight: bold;
          }}
        </style>
      </head>
      <body>
        <h2>Gracias por tu compra en Turify, {nombre} 🎉</h2>
        <p>Pedido <strong>#{numero_pedido}</strong></p>
        <table>
          <thead>
            <tr>
              <th>Servicio</th>
              <th>Categoría</th>
              <th>Cantidad</th>
              <th>Precio</th>
              <th>Subtotal</th>
            </tr>
          </thead>
          <tbody>
            {filas}
          </tbody>
        </table>
        <p class="totales">Subtotal: ${subtotal}</p>
        <p class="totales">IVA (21%): ${iva}</p>
        <p class="totales">Total: ${total}</p>
        <br>
        <p>📍 Dirección de entrega: {direccion}</p>
        <p>📅 Fecha de pedido: {fecha}</p>
        <br>
        <p>Ante cualquier duda, escribinos. ¡Gracias por confiar en nosotros!<br>— El equipo de Turify</p>
      </body>
    </html>
    """
    return html

def enviar_mail_confirmacion(destinatario: str, nombre: str, numero_pedido: str, detalles: list, direccion: str, fecha: str):
    remitente = "turifycontacto@gmail.com"
    password = "sgls ribs ahwh tmeo"
    asunto = "Confirmación de tu pedido en Turify ✈️"

    html = generar_html_confirmacion(nombre, numero_pedido, detalles, direccion, fecha)

    msg = MIMEMultipart("alternative")
    msg["From"] = remitente
    msg["To"] = destinatario
    msg["Subject"] = asunto

    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remitente, password)
            servidor.sendmail(remitente, destinatario, msg.as_string())
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
