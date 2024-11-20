import time
import os
import getpass
import pickle
import pyotp
import imaplib
import email
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuración para manejar cookies y autenticación
COOKIES_FILE = "session_cookies.pkl"
SECRET_KEY = "TU_CLAVE_SECRETA_2FA"  # Clave secreta del 2FA (si la tienes)
IMAP_SERVER = "imap.gmail.com"       # Servidor de correo IMAP
EMAIL = "tu_email@gmail.com"         # Tu correo electrónico
EMAIL_PASSWORD = "tu_password"       # Contraseña del correo

# Configuración del navegador y opciones
base_download_dir = os.path.join(os.getcwd(), "Descargas")
if not os.path.exists(base_download_dir):
    os.makedirs(base_download_dir)

chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": base_download_dir,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True,
}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(120)

# Funciones de manejo de cookies
def save_cookies(driver, path):
    with open(path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)

def load_cookies(driver, path):
    with open(path, "rb") as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)

# Función para generar un código TOTP con pyotp
def generate_totp(secret_key):
    totp = pyotp.TOTP(secret_key)
    return totp.now()

# Función para extraer el código de 2FA del correo electrónico
def get_2fa_code_from_email():
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, EMAIL_PASSWORD)
        mail.select("inbox")
        status, messages = mail.search(None, 'FROM "no-reply@example.com" SUBJECT "Código de seguridad"')
        mail_ids = messages[0].split()
        latest_email_id = mail_ids[-1]
        status, data = mail.fetch(latest_email_id, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode().strip()
        else:
            return msg.get_payload(decode=True).decode().strip()
    except Exception as e:
        print(f"Error al obtener el código 2FA del correo: {e}")
        return None

# Flujo principal del script
try:
    print("Iniciando sesión...")
    driver.get("https://bullmarketbrokers.com/Security/SignIn")
    
    # Cargar cookies si están disponibles
    if os.path.exists(COOKIES_FILE):
        load_cookies(driver, COOKIES_FILE)
        driver.refresh()
        time.sleep(5)
        print("Sesión restaurada con cookies existentes.")
    else:
        # Inicio de sesión manual si no hay cookies
        email = input("Ingresa tu email: ")
        password = getpass.getpass("Ingresa tu contraseña: ")

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "Email"))).send_keys(email)
        driver.find_element(By.NAME, "Password").send_keys(password)
        driver.find_element(By.ID, "submitButton").click()

        # Esperar a que aparezca el campo de 2FA
        otp_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "2fa_field_id")))  # Cambia el ID
        code_2fa = None

        # Generar código 2FA automáticamente (si se usa TOTP)
        if SECRET_KEY:
            code_2fa = generate_totp(SECRET_KEY)
            print(f"Código TOTP generado: {code_2fa}")
        else:
            # Obtener código 2FA desde el correo electrónico
            print("Obteniendo el código 2FA desde el correo electrónico...")
            code_2fa = get_2fa_code_from_email()

        if code_2fa:
            otp_field.send_keys(code_2fa)
            driver.find_element(By.ID, "submit_otp_button_id").click()  # Cambia el ID

        # Guardar cookies para futuras sesiones
        save_cookies(driver, COOKIES_FILE)
        print("Sesión iniciada y cookies guardadas.")

    # Continuar con la navegación después del inicio de sesión
    print("Accediendo a la página de balance...")
    driver.get("https://bullmarketbrokers.com/Clients/accountbalance")

    # Aquí puedes continuar con el flujo de tu script, como descargar archivos.

except Exception as e:
    print(f"Ocurrió un error durante el proceso: {e}")
    driver.save_screenshot('error_screenshot.png')
    print("Captura de pantalla guardada como error_screenshot.png")

finally:
    driver.quit()
    print("Proceso completado.")
