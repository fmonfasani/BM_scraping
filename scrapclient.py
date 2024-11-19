import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def iniciar_sesion(driver, email, password):
    """
    Inicia sesión en el sitio web.
    """
    print("Iniciando sesión...")
    driver.get("https://bullmarketbrokers.com/Security/SignIn")  # URL de inicio de sesión
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "Email"))).send_keys(email)
    driver.find_element(By.NAME, "Password").send_keys(password)
    driver.find_element(By.ID, "submitButton").click()
    
    # Esperar hasta que la URL cambie indicando éxito en el login
    WebDriverWait(driver, 60).until(EC.url_contains("/Clients"))
    print("Sesión iniciada con éxito.")

def manejar_2fa(driver):
    """
    Maneja pasos adicionales de autenticación (si los hay).
    """
    try:
        print("Verificando autenticación de dos factores...")
        # Aquí puedes manejar el 2FA si aparece un campo adicional para ingresar un código
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "2fa_input"))  # Cambia al ID real del campo de código
        ).send_keys("TU_CODIGO_2FA")  # Puedes usar un input para capturar el código
        driver.find_element(By.ID, "2fa_submit_button").click()  # Cambia al ID real del botón
        print("Autenticación de dos factores completada.")
    except Exception:
        print("No se detectó autenticación de dos factores. Continuando...")

def obtener_cuentas(driver):
    """
    Scrapea la lista de cuentas después de iniciar sesión.
    """
    print("Obteniendo lista de cuentas...")
    cuentas = []
    driver.get("https://bullmarketbrokers.com/Clients/AccountList")  # Cambia a la URL real donde están las cuentas

    # Esperar a que la lista de cuentas esté cargada
    cuentas_elementos = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".account-row"))  # Ajusta el selector al HTML real
    )

    # Extraer datos de cada cuenta
    for elemento in cuentas_elementos:
        account_id = elemento.get_attribute("data-id")
        account_text = elemento.find_element(By.CLASS_NAME, "account-text").text
        account_number = elemento.find_element(By.CLASS_NAME, "account-number").text
        cuentas.append({
            "id": int(account_id),
            "text": account_text,
            "number": int(account_number)
        })

    return cuentas

def guardar_en_json(data, archivo):
    """
    Guarda los datos en un archivo JSON.
    """
    with open(archivo, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Configuración de Selenium
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": "./Descargas",  # Configurar la carpeta de descargas
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True
}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)

try:
    email = "marcelolezcano_17@hotmail.com"  # Reemplaza con tu correo
    password = "Inversiones24$"       # Reemplaza con tu contraseña

    # Iniciar sesión
    iniciar_sesion(driver, email, password)

    # Manejar autenticación de dos factores (si aplica)
    manejar_2fa(driver)

    # Scraping después del inicio de sesión
    cuentas = obtener_cuentas(driver)

    # Guardar los datos en un archivo JSON
    guardar_en_json(cuentas, "clientes.json")
    print("Cuentas guardadas en clientes.json")

except Exception as e:
    print(f"Ocurrió un error: {e}")

finally:
    driver.quit()
    print("Navegador cerrado.")
