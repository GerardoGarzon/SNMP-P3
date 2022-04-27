import imghdr
import smtplib
from email.message import EmailMessage

mail_sender = "test.redes.escom@gmail.com"
mail_server = 'smtp.gmail.com'
password = 'pichicato123'


def send_alert_attached(subject, img_path, ip_address, type_data):
    message = EmailMessage()
    message['Subject'] = subject
    message['From'] = mail_sender
    message['To'] = mail_sender
    message.set_content("Se exedio el limite del umbral para " + type_data + " del dispositivo con ip " + ip_address)

    with open(img_path, 'rb') as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name

    message.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

    with smtplib.SMTP_SSL(mail_server, 465) as smtp:
        smtp.login(mail_sender, password)
        smtp.send_message(message)


# send_alert_attached("Warning!", "data/devices_files/192.168.1.130/detectionCPU.png", "192.168.1.130", "CPU")
