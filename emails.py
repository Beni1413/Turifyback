import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_mail_confirmacion(destinatario: str, nombre: str, numero_pedido: str):
    remitente = "viceensanchh@gmail.com"
    password = "wkmu kasy rvyr uutx" 
    asunto = "Pedido confirmado"
    
    cuerpo = f"""
    Hola {nombre},

    Tu pedido número {numero_pedido} ha sido confirmado exitosamente.
    Gracias por confiar en nosotros 🛍️
    Saludos,
    El equipo de Turify
    """

    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(cuerpo, 'plain'))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
            servidor.login(remitente, password)
            servidor.sendmail(remitente, destinatario, msg.as_string())
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
