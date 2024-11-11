import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import getpass
from datetime import datetime
import requests

def check_internet_connection(url="https://www.google.com", timeout=5):
    """Verifica la conexión a Internet."""
    try:
        requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        return False

def init_chrome_driver(download_dir):
    """Inicializa el navegador Chrome con opciones y control de errores."""
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(120)
        return driver
    except Exception as e:
        print(f"Error al iniciar ChromeDriver: {e}")
        return None

start_time = time.time()

# Configuración de descarga y opciones de Chrome
base_download_dir = os.path.join(os.getcwd(), "Descargas_PDFs")
os.makedirs(base_download_dir, exist_ok=True)

# Verificar la conexión a Internet
if not check_internet_connection():
    print("No hay conexión a Internet. Por favor, verifica tu conexión y vuelve a intentarlo.")
    exit()

# Inicializar ChromeDriver
driver = init_chrome_driver(base_download_dir)
if driver is None:
    print("No se pudo iniciar ChromeDriver. Verifica que esté instalado correctamente.")
    exit()

# Credenciales de inicio de sesión
email = "marcelolezcano_17@hotmail.com"
password = getpass.getpass("Ingresa tu contraseña: ")

# Cargar lista de cuentas de usuario desde el archivo JSON
with open("usuarios.json", "r") as file:
    stock_accounts = json.load(file)

try:
    print("Iniciando sesión...")
    driver.get("https://bullmarketbrokers.com/Security/SignIn")
    
    # Esperar y completar el formulario de inicio de sesión
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "Email"))).send_keys(email)
    driver.find_element(By.NAME, "Password").send_keys(password)
    driver.find_element(By.ID, "submitButton").click()
    
    # Espera a que se redirija a la página de balance
    WebDriverWait(driver, 30).until(EC.url_contains("/Clients/accountbalance"))
    print("Accediendo a la página de balance...")

    # Extraer información de los usuarios cargados
    clientes = []
    for account in stock_accounts:
        cliente_nombre = account["text"]
        cliente_number = account["number"]

        print(f"Extrayendo información para el usuario {cliente_nombre}...")

        # Añadir la información del cliente al JSON
        cliente_info = {
            "nombre": cliente_nombre,
            "número": cliente_number,
        }
        clientes.append(cliente_info)
    
    # Guardar en un archivo JSON llamado "clientes.json"
    with open("clientes.json", "w") as outfile:
        json.dump(clientes, outfile, indent=4, ensure_ascii=False)
    
    print("Información de los clientes guardada en 'clientes.json'.")

except Exception as e:
    print(f"Ocurrió un error durante el proceso: {e}")
    driver.save_screenshot('error_screenshot.png')
    print("Captura de pantalla guardada como error_screenshot.png")

finally:
    driver.quit()
    print("Proceso completado")

    end_time = time.time()
    elapsed_time_minutes = (end_time - start_time)
