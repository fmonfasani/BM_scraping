from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import getpass
from datetime import datetime

# Configuración de descarga y opciones de Chrome
download_dir = os.path.join(os.getcwd(), "Descargas_PDFs")
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True,
}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(120)

# Credenciales de inicio de sesión
email = "marcelolezcano_17@hotmail.com"
password = getpass.getpass("Ingresa tu contraseña: ")

# Lista de monedas y sus IDs de botón
monedas = {
    "PESOS": "btn_filter_pesos",
    "DÓLARES": "btn_filter_dolares",
    "DÓLARES CABLE": "btn_filter_dolares_cable"
}

# Lista de cuentas de usuario
stock_accounts = [
    {"text": "LEZCANO JUAN MARCELO - Catalaxia SA", "number": "13641"},
    {"text": "Wichmann, Maria Alejandra", "number": "15154"},
    # Agrega más usuarios aquí
]

# Fechas para el reporte
fecha_inicio = "01/01/2024"
fecha_fin = "31/01/2024"
fecha_nombre = "ENERO24"  # para usar en el nombre del archivo

# Función para esperar hasta que el archivo esté completamente disponible
def esperar_descarga_completa(nombre_base, tiempo_espera=120):
    tiempo_inicial = time.time()
    while True:
        archivos_temporales = [
            f for f in os.listdir(download_dir) 
            if f.startswith(nombre_base) and (f.endswith('.crdownload') or f.endswith('.tmp'))
        ]
        if not archivos_temporales:
            try:
                latest_file = max([os.path.join(download_dir, f) for f in os.listdir(download_dir)], key=os.path.getctime)
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
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "Email"))).send_keys(email)
    driver.find_element(By.NAME, "Password").send_keys(password)
    driver.find_element(By.ID, "submitButton").click()
    time.sleep(10)  # Espera para la autenticación de dos factores si es necesario

    print("Accediendo a la página de balance...")
    driver.get("https://bullmarketbrokers.com/Clients/accountbalance")

    for account in stock_accounts:
        cliente_nombre = account["text"]
        cliente_number = account["number"]

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
                os.rename(latest_file, os.path.join(download_dir, new_file_name))
                print(f"Archivo renombrado a: {new_file_name}")
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
