import time
import os
import getpass
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuración para manejar cookies
COOKIES_FILE = "session_cookies.pkl"

# Configuración del navegador y opciones
chrome_options = webdriver.ChromeOptions()
prefs = {
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
        email = "marcelolezcano_17@hotmail.com"
        password = "Inversiones24$"

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "Email"))).send_keys(email)
        driver.find_element(By.NAME, "Password").send_keys(password)
        driver.find_element(By.ID, "submitButton").click()

        # Esperar a que aparezca el campo de 2FA
        try:
            otp_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "2fa_field_id"))  # Ajusta el ID según la plataforma
            )
            print("Se requiere autenticación de segundo factor.")
            code = input("Ingresa el código de 2FA: ")
            otp_field.send_keys(code)
            driver.find_element(By.ID, "submit_otp_button_id").click()  # Ajusta el ID según la plataforma
        except:
            print("No se detectó autenticación de segundo factor.")

        # Guardar cookies para futuras sesiones
        save_cookies(driver, COOKIES_FILE)
        print("Sesión iniciada y cookies guardadas.")

    # Validar que se accedió correctamente
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print("Inicio de sesión exitoso.")

except Exception as e:
    print(f"Ocurrió un error durante el proceso: {e}")
    driver.save_screenshot('error_screenshot.png')
    print("Captura de pantalla guardada como error_screenshot.png")

finally:
    driver.quit()
    print("Proceso completado.")
