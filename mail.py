from flask_mail import Mail, Message


def init_app(app):
    global mail

    mail = Mail(app)


def send_email(text_body, subject, recipients=['witetrashd@gmail.com']):
    message = Message(subject=subject, recipients=recipients)
    message.body = text_body
    # message.html = html_body

    mail.send(message)
