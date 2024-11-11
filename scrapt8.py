import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import getpass
from datetime import datetime

start_time = time.time()

# Configuración de descarga y opciones de Chrome
base_download_dir = os.path.join(os.getcwd(), "Descargas_PDFs")
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

# Credenciales de inicio de sesión
email = "marcelolezcano_17@hotmail.com"
password = getpass.getpass("Ingresa tu contraseña: ")

# Cargar lista de cuentas de usuario desde el archivo JSON
with open("usuarios.json", "r") as file:
    stock_accounts = json.load(file)

# Lista de monedas y sus IDs de botón
monedas = {
    "PESOS": "btn_filter_pesos",
    "DÓLARES": "btn_filter_dolares",
    "DÓLARES CABLE": "btn_filter_dolares_cable"
}

# Fechas para el reporte
fecha_inicio = "01/01/2024"
fecha_fin = "31/10/2024"
fecha_nombre = "Reporte_2024"  # para usar en el nombre del archivo

# Función para esperar hasta que el archivo esté completamente disponible
def esperar_descarga_completa(nombre_base, tiempo_espera=120):
    tiempo_inicial = time.time()
    while True:
        archivos_temporales = [
            f for f in os.listdir(base_download_dir)
            if f.startswith(nombre_base) and not f.endswith('.crdownload') and not f.endswith('.tmp')
        ]
        if archivos_temporales:
            latest_file = max([os.path.join(base_download_dir, f) for f in archivos_temporales], key=os.path.getctime)
            try:
                with open(latest_file, 'rb'):
                    return latest_file
            except (PermissionError, FileNotFoundError):
                pass

        if time.time() - tiempo_inicial > tiempo_espera:
            print(f"No se pudo acceder al archivo después de {tiempo_espera} segundos.")
            return None
        time.sleep(1)

try:
    print("Iniciando sesión...")
    driver.get("https://bullmarketbrokers.com/Security/SignIn")
    
    # Esperar y completar el formulario de inicio de sesión
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.NAME, "Email"))).send_keys(email)
    driver.find_element(By.NAME, "Password").send_keys(password)
    driver.find_element(By.ID, "submitButton").click()
    time.sleep(10)  # Espera para la autenticación de dos factores si es necesario

    print("Accediendo a la página de balance...")
    driver.get("https://bullmarketbrokers.com/Clients/accountbalance")

    for account in stock_accounts:
        cliente_nombre = account["text"]
        cliente_number = account["number"]

        # Crear una carpeta específica para el usuario en `download_dir`
        user_download_dir = os.path.join(base_download_dir, f"{cliente_nombre.replace(' ', '_')}({cliente_number})")
        if not os.path.exists(user_download_dir):
            os.makedirs(user_download_dir)
        
        print(f"Seleccionando cuenta para el usuario {cliente_nombre}...")
        account_selector = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.select2-container a.select2-choice"))
        )
        
        # Hacer clic en el selector para abrir el menú desplegable
        account_selector.click()
        time.sleep(1)

        # Seleccionar la cuenta específica
        desired_account = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@class='select2-result-label' and contains(text(), '{cliente_number}')]"))
        )
        driver.execute_script("arguments[0].click();", desired_account)
        print(f"Usuario seleccionado: {cliente_number} {cliente_nombre}")
        
        # Cerrar el menú desplegable
        driver.find_element(By.CSS_SELECTOR, "body").click()
        time.sleep(1)

        # Configurar fechas de inicio y fin para el reporte
        print("Estableciendo las fechas de búsqueda...")
        start_date = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "txt_AccountBalance_SearchStartDate")))
        start_date.clear()
        start_date.send_keys(fecha_inicio)
        
        end_date = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "txt_AccountBalance_SearchEndDate")))
        end_date.clear()
        end_date.send_keys(fecha_fin)

        # Iniciar la búsqueda para cada moneda
        for moneda, boton_id in monedas.items():
            print(f"Seleccionando la moneda: {moneda}...")
            currency_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, boton_id)))
            driver.execute_script("arguments[0].click();", currency_button)
            time.sleep(2)

            print(f"Descargando archivo de Excel para {moneda}...")
            download_link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Descargar Excel')]"))
            )
            download_link.click()

            latest_file = esperar_descarga_completa("Cuenta Corriente")

            if latest_file:
                new_file_name = f"{cliente_number}_{cliente_nombre.replace(' ', '_')}_CC_{moneda}_{fecha_nombre}.xls"
                os.rename(latest_file, os.path.join(user_download_dir, new_file_name))
                print(f"Archivo renombrado y movido a la carpeta: {new_file_name}")
            else:
                print(f"Error al renombrar el archivo para {moneda} en cuenta {cliente_nombre}.")

        time.sleep(3)  # Esperar un momento antes de pasar a la siguiente cuenta

except Exception as e:
    print(f"Ocurrió un error durante el proceso: {e}")
    driver.save_screenshot('error_screenshot.png')
    print("Captura de pantalla guardada como error_screenshot.png")

finally:
    driver.quit()
    print("Proceso completado")

    end_time = time.time()
    elapsed_time_minutes = (end_time - start_time) / 60
    elapsed_time = elapsed_time_minutes * 60
    print(f"Tiempo transcurrido: {elapsed_time_minutes:.2f} minutos")
    print(f"Tiempo total de ejecución: {elapsed_time:.2f} segundos")
