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

# Datos del cliente
email = "marcelolezcano_17@hotmail.com"
password = getpass.getpass("Ingresa tu contraseña: ")
cliente_id = "15154"
cliente_nombre = "Wichmann_Maria_Eugenia"

# Lista de monedas y sus IDs de botón
monedas = {
    "PESOS": "btn_filter_pesos",
    "DÓLARES": "btn_filter_dolares",
    "DÓLARES CABLE": "btn_filter_dolares_cable"
}

# Fecha para el nombre del archivo
fecha_nombre = "ENERO24"

try:
    print("Iniciando sesión...")
    driver.get("https://bullmarketbrokers.com/Security/SignIn")
    
    # Esperar y completar el formulario de inicio de sesión
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "Email"))).send_keys(email)
    driver.find_element(By.NAME, "Password").send_keys(password)
    driver.find_element(By.ID, "submitButton").click()
    
    # Esperar a que se cargue la página principal
    print("Esperando a que se cargue la página principal...")
    WebDriverWait(driver, 10).until(EC.url_changes("https://bullmarketbrokers.com/Security/SignIn"))

    print("Accediendo a la página de balance...")
    driver.get("https://bullmarketbrokers.com/Clients/accountbalance")
    
    # Esperar que el selector de cuentas esté visible
    print("Esperando el selector de cuentas...")
    account_selector = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.select2-container a.select2-choice"))
    )
    
    # Hacer clic en el selector para abrir el menú desplegable
    print("Haciendo clic en el selector de cuentas...")
    account_selector.click()
    time.sleep(2)  # Pausa para permitir que el menú se despliegue

    # Seleccionar la cuenta específica por el texto visible
    print("Buscando y seleccionando el usuario específico...")
    desired_account = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='select2-result-label' and contains(text(), '15154 Wichmann, Maria Alejandra')]"))
    )
    driver.execute_script("arguments[0].click();", desired_account)
    print("Usuario seleccionado: 15154 Wichmann, Maria Alejandra")
    
    # Cerrar el menú superpuesto haciendo clic en el fondo
    print("Cerrando el menú desplegable...")
    driver.find_element(By.CSS_SELECTOR, "body").click()
    time.sleep(1)

    # Iterar sobre cada moneda y realizar la descarga
    for moneda, boton_id in monedas.items():
        print(f"Seleccionando la moneda: {moneda}...")
        currency_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, boton_id))
        )
        
        # Hacer clic en el botón de moneda
        driver.execute_script("arguments[0].click();", currency_button)
        time.sleep(1)  # Espera para que la moneda se cargue

        # Selección de la fecha de inicio
        print("Estableciendo la fecha de inicio...")
        start_date = driver.find_element(By.ID, "txt_AccountBalance_SearchStartDate")
        start_date.clear()
        start_date.send_keys("01/01/2024")  # Cambia la fecha de inicio según tus necesidades

        # Selección de la fecha de fin
        print("Estableciendo la fecha de fin...")
        end_date = driver.find_element(By.ID, "txt_AccountBalance_SearchEndDate")
        end_date.clear()
        end_date.send_keys("31/01/2024")  # Cambia la fecha de fin según tus necesidades

        # Iniciar la descarga del archivo de Excel
        print(f"Descargando archivo de Excel para {moneda}...")
        download_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Descargar Excel')]"))
        )
        download_link.click()
        time.sleep(5)  # Espera para que la descarga se complete

        # Renombrar el archivo descargado
        print(f"Renombrando el archivo descargado para {moneda}...")
        latest_file = max([os.path.join(download_dir, f) for f in os.listdir(download_dir)], key=os.path.getctime)
        new_file_name = f"{cliente_id}_{cliente_nombre}_CC_{moneda}_{fecha_nombre}.xls"
        os.rename(latest_file, os.path.join(download_dir, new_file_name))
        print(f"Archivo renombrado a: {new_file_name}")

except Exception as e:
    print(f"Ocurrió un error durante el proceso: {e}")
    driver.save_screenshot('error_screenshot.png')  # Captura de pantalla en caso de error
    print("Captura de pantalla guardada como error_screenshot.png")

finally:
    driver.quit()
    print("Proceso completado")
