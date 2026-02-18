from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiosmtplib
from core.config import config

async def send_confirmation_email(recipient: str, username: str, verification_code: int):
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #4CAF50; padding: 20px; text-align: center;">
                <h1 style="color: white;">Welcome!</h1>
            </div>
            <div style="padding: 20px;">
                <h2>Hello, {username}!</h2>
                <p>Thank you for registering with our service.</p>
                <p>Please confirm your email address by clicking the button below:</p>
                <div style="text-align: center; margin: 30px 0;">
                    You're verification code for registration: <span>{verification_code}</span>
                </div>
                <p style="color: #666; font-size: 14px;">
                    This link will expire in 24 hours.<br>
                    If you didn't create an account, please ignore this email.
                </p>
            </div>
            <div style="background-color: #f4f4f4; padding: 10px; text-align: center; font-size: 12px; color: #666;">
                <p>&copy; 2026 Your Company. All rights reserved.</p>
            </div>
        </body>
    </html>
    """
    
    message = MIMEMultipart()
    message['From'] = config.SMTP_EMAIL
    message['To'] = recipient
    message['Subject'] = "Confirm Your Email Address"
    message.attach(MIMEText(html_body, 'html'))
    
    try:
        # Используем контекстный менеджер для соединения
        async with aiosmtplib.SMTP(
            hostname=config.SMTP_SERVER,
            port=config.SMTP_PORT,
            start_tls=True
        ) as smtp:
            await smtp.login(config.SMTP_EMAIL, config.SMTP_PASSWORD)
            await smtp.send_message(message)
        
        print(f"✅ Email sent to {recipient}")
        return True
    except Exception as e:
        print(f"❌ Error sending email to {recipient}: {e}")
        return False


async def send_password_change_code_email(recipient: str, username: str, verification_code: int):
    """Отправка кода подтверждения для смены пароля на email."""
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background-color: #1a1a2e; padding: 20px; text-align: center;">
                <h1 style="color: white;">Смена пароля</h1>
            </div>
            <div style="padding: 20px;">
                <h2>Здравствуйте, {username}!</h2>
                <p>Вы запросили изменение пароля. Используйте код ниже на странице профиля:</p>
                <div style="text-align: center; margin: 30px 0; padding: 20px; background: #f4f4f4; border-radius: 12px;">
                    <span style="font-size: 28px; font-weight: bold; letter-spacing: 6px;">{verification_code}</span>
                </div>
                <p style="color: #666; font-size: 14px;">
                    Код действителен 15 минут.<br>
                    Если вы не запрашивали смену пароля, проигнорируйте это письмо.
                </p>
            </div>
            <div style="background-color: #f4f4f4; padding: 10px; text-align: center; font-size: 12px; color: #666;">
                <p>&copy; 2026 Ваш сервис. Все права защищены.</p>
            </div>
        </body>
    </html>
    """
    message = MIMEMultipart()
    message["From"] = config.SMTP_EMAIL
    message["To"] = recipient
    message["Subject"] = "Код для смены пароля"
    message.attach(MIMEText(html_body, "html"))
    try:
        async with aiosmtplib.SMTP(
            hostname=config.SMTP_SERVER,
            port=config.SMTP_PORT,
            start_tls=True,
        ) as smtp:
            await smtp.login(config.SMTP_EMAIL, config.SMTP_PASSWORD)
            await smtp.send_message(message)
        print(f"✅ Password change code email sent to {recipient}")
        return True
    except Exception as e:
        print(f"❌ Error sending password code email to {recipient}: {e}")
        return False