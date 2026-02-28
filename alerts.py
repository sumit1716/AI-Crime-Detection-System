import smtplib
from email.message import EmailMessage

def send_crime_alert(image_path):
    msg = EmailMessage()
    msg['Subject'] = '⚠️ CRIME ALERT DETECTED!'
    msg['From'] = 'your_email@gmail.com'
    msg['To'] = 'police_station@gmail.com'
    msg.set_content('Suspicious activity detected. Check the attached image.')

    with open(image_path, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='image', subtype='jpeg', filename='incident.jpg')

    # Gmail SMTP setup (App Password use karna padega)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('your_email@gmail.com', 'your_app_password')
        smtp.send_message(msg)