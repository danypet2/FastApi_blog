import smtplib
from email.message import EmailMessage
from src.celery_app import celery
from src.config import SMTP_PORT, SMTP_HOST, SMTP_USER, SMTP_PASSWORD


def email_verification(user_email: str, token: str):
    email = EmailMessage()
    email['Subject'] = 'Подтвердите почту!'
    email['From'] = SMTP_USER
    email['To'] = user_email

    email.set_content(
        '<div>'
        f'<h1 style="color: black;">Здравствуйте, Подтвердите вашу почту! Ваш проверочный код: </p>{token}</p></p>😊</h1>'
        '</div>',
        subtype='html'
    )
    return email


def email_after_registration(username: str, user_email: str):
    email = EmailMessage()
    email['Subject'] = 'Регистрация успешна!'
    email['From'] = SMTP_USER
    email['To'] = user_email

    email.set_content(
        '<div>'
        f'<h1 style="color: black;">Здравствуйте, {username}, Вы успешно зарегистрировались на нашем сайте, для полного доступа к его функциональностям, просим подтвердить почту!)</h1>'
        '</div>',
        subtype='html'
    )
    return email


def email_after_verify( user_email: str):
    email = EmailMessage()
    email['Subject'] = 'Вы подтвердили адрес электронной почты!!'
    email['From'] = SMTP_USER
    email['To'] = user_email

    email.set_content(
        '<div>'
        f'<h1 style="color: black;">Здравствуйте, вы успешно подтвердили адрес электронной почты! И теперь вам доступен весь функционал сайта!</h1>'
        '</div>',
        subtype='html'
    )
    return email


def email_forgot_password(username: str, user_email: str, token: str):
    email = EmailMessage()
    email['Subject'] = 'Сброс пароля'
    email['From'] = SMTP_USER
    email['To'] = user_email

    email.set_content(
        '<div>'
        f'<h1 style="color: black;">Здравствуйте, {username}, Подтвердите сброс вашего пароля! Перейдите по следующей ссылки: <p>http://127.0.0.1:8000/auth/reset-password?{token}</p>😊</h1>'
        '</div>',

        subtype='html'
    )
    return email


@celery.task
def send_email_verification(user_email: str, token: int):
    email = email_verification(user_email, token)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)


@celery.task
def send_email_forgot_password(username: str, user_email: str, token: str):
    email = email_forgot_password(username, user_email, token)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)


@celery.task
def send_email_after_register(username: str, user_email: str):
    email = email_after_registration(username, user_email)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)


@celery.task
def send_email_after_verify(user_email: str):
    email = email_after_verify(user_email)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
