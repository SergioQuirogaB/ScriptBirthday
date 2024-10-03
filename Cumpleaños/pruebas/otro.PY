import json
import smtplib
import time
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import schedule


def load_clients():
    """Carga la lista de clientes desde un archivo JSON."""
    with open('otro.json', 'r') as file:
        return json.load(file)

def send_birthday_email(client):
    #Envía un correo electrónico de cumpleaños al cliente con copia a una lista de correo
    sender_email = "magicandy2023@gmail.com"
    sender_password = "gsnu kupj fklj njtl"  
    # Asegúrate de usar una contraseña específica para la aplicación si es necesario

    receiver_email = client["email"]

    # Obtener la lista de correos en copia (CC) del cliente, si existe
    cc_emails = client.get("cc", [])  # Si no hay 'cc', será una lista vacía

    # Crear el mensaje
    msg = MIMEMultipart("related")
    msg["Subject"] = "¡Feliz Cumpleaños!"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    if cc_emails:
        msg["Cc"] = ", ".join(cc_emails)  # Agregar los destinatarios en copia

    # Contenido HTML del correo con la imagen incrustada y borde verde
    html_content = f"""
    <html>
        <head>
            <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333333;
            }}
            .container {{
                width: 70%;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #F0FCF2;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border: 3px solid #165128;  /* Borde verde */
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .header h1 {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 1.5em;
                margin: 0;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                font-size: 0.9em;
                color: #777777;
            }}
            .confetti-link {{
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }}
            .confetti-link:hover {{
                background-color: #45a049;
            }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 <strong>{client["name"]}</strong> 🎉</h1>
                    <img src="cid:image1" alt="Tarjeta de Cumpleaños" style="width:100%;max-width:600px;">
                </div>
            </div>

        </body>
    </html>
    """

    part1 = MIMEText(html_content, "html")
    msg.attach(part1)

    # Adjuntar la imagen con Content-ID
    with open(r"C:\Users\Usuario\Desktop\Cumpleaños\TarjetaCumpleañosTF.gif", "rb") as image_file:
        image = MIMEImage(image_file.read())
        image.add_header('Content-ID', '<image1>')
        msg.attach(image)

    # Enviar el correo
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            # Destinatarios (para y CC)
            all_recipients = [receiver_email] + cc_emails
            server.sendmail(sender_email, all_recipients, msg.as_string())
            print(f"Correo enviado a {client['name']} ({client['email']}) con copia a: {', '.join(cc_emails) if cc_emails else 'No hay CC'}")
    except Exception as e:
        print(f"Error al enviar el correo a {client['name']} ({client['email']}): {e}")

def check_birthdays():
    #Verifica si hoy es el cumpleaños de algún cliente y envía el correo correspondiente
    clients = load_clients()
    today = datetime.today().strftime("%m-%d")
    for client in clients:
        if client["birthday"] == today:
            send_birthday_email(client)

if __name__ == "__main__":
    # Programa la tarea para que se ejecute diariamente a las 08:15
    schedule.every().day.at("10:37").do(check_birthdays)

    while True:
        schedule.run_pending()
        time.sleep(60)