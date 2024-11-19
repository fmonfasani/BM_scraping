
    


import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

def iniciar_sesion(driver, email, password):
    """
    Inicia sesión en el sitio web y maneja el flujo inicial.
    """
    print("Iniciando sesión...")
    try:
        driver.get("https://bullmarketbrokers.com/Security/SignIn")
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "Email"))).send_keys(email)
        driver.find_element(By.NAME, "Password").send_keys(password)
        driver.find_element(By.ID, "submitButton").click()

        # Espera a que la redirección sea exitosa
        WebDriverWait(driver, 60).until(EC.url_contains("/Clients"))
        print("Sesión iniciada con éxito.")
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        driver.quit()
        exit()

def manejar_2fa(driver):
    """
    Maneja pasos adicionales de autenticación (si los hay).
    """
    try:
        print("Verificando autenticación de dos factores...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "2fa_input"))  # Cambia este selector según sea necesario
        ).send_keys("TU_CODIGO_2FA")  # Reemplaza con el código correcto
        driver.find_element(By.ID, "2fa_submit_button").click()  # Cambia este selector según sea necesario
        print("Autenticación de dos factores completada.")
    except Exception:
        print("No se detectó autenticación de dos factores. Continuando...")

def verificar_ventana(driver):
    """
    Verifica si el navegador aún está abierto.
    """
    if not driver.window_handles:
        print("El navegador se cerró inesperadamente.")
        driver.quit()
        exit()

def obtener_cuentas(driver):
    """
    Scrapea la lista de cuentas después de iniciar sesión.
    """
    try:
        print("Obteniendo lista de cuentas...")
        driver.get("https://bullmarketbrokers.com/Clients/AccountList")
        verificar_ventana(driver)

        cuentas_elementos = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".account-row"))
        )

        cuentas = []
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
    except Exception as e:
        print(f"Error al obtener cuentas: {e}")
        driver.quit()
        exit()

def guardar_en_json(data, archivo):
    """
    Guarda los datos en un archivo JSON.
    """
    try:
        with open(archivo, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar JSON: {e}")

# Configuración de Selenium
chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": "./Descargas",  # Cambiar al directorio de descargas deseado
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True
}
chrome_options.add_experimental_option("prefs", prefs)

# Opcional: Ejecutar en modo sin cabeza para mayor estabilidad
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

try:
    email = "marcelolezcano_17@hotmail.com"  # Reemplaza con tu correo
    password = "Inversiones24$"       # Reemplaza con tu contraseña

    # Iniciar sesión
    iniciar_sesion(driver, email, password)

    # Manejar autenticación de dos factores si es necesario
    manejar_2fa(driver)

    # Scraping después del inicio de sesión
    cuentas = obtener_cuentas(driver)

    # Guardar los datos en un archivo JSON
    guardar_en_json(cuentas, "clientes.json")
    print("Cuentas guardadas en clientes.json")

except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")

finally:
    driver.quit()
    print("Navegador cerrado.")
