from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import getpass

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

# Datos de la cuenta
usuarios = [
    {"id": "15154", "nombre": "Wichmann_Maria_Eugenia"},
    # Agrega más usuarios aquí
]

# Función para formatear la fecha si es necesario
def formatear_fecha(fecha):
    if len(fecha) == 8 and fecha.isdigit():  # Si es formato 01102024
        return f"{fecha[:2]}/{fecha[2:4]}/{fecha[4:]}"
    return fecha  # Si ya está en formato correcto, no hace nada

# Solicitar fechas al usuario y formatearlas
fecha_inicio = formatear_fecha(input("Ingresa la fecha de inicio (DD/MM/AAAA): "))
fecha_fin = formatear_fecha(input("Ingresa la fecha de fin (DD/MM/AAAA): "))

# Lista de monedas y sus IDs de botón
monedas = {
    "PESOS": "btn_filter_pesos",
    "DÓLARES": "btn_filter_dolares",
    "DÓLARES CABLE": "btn_filter_dolares_cable"
}

# Credenciales de inicio de sesión
email = "marcelolezcano_17@hotmail.com"
password = getpass.getpass("Ingresa tu contraseña: ")

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

    for usuario in usuarios:
        cliente_id = usuario["id"]
        cliente_nombre = usuario["nombre"]

        # Esperar que el selector de cuentas esté visible
        print(f"Seleccionando cuenta para el usuario {cliente_nombre}...")
        account_selector = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.select2-container a.select2-choice"))
        )
        
        # Hacer clic en el selector para abrir el menú desplegable
        account_selector.click()
        time.sleep(1)

        # Seleccionar la cuenta específica por el texto visible
        desired_account = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@class='select2-result-label' and contains(text(), '{cliente_id} {cliente_nombre.split('_')[0]}')]"))
        )
        driver.execute_script("arguments[0].click();", desired_account)
        print(f"Usuario seleccionado: {cliente_id} {cliente_nombre.replace('_', ' ')}")
        
        # Cerrar el menú superpuesto haciendo clic en el fondo
        driver.find_element(By.CSS_SELECTOR, "body").click()
        time.sleep(1)

        # Configurar fechas para el usuario actual
        print("Estableciendo las fechas...")
        
        # Espera explícita para el campo de fecha de inicio
        start_date = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "txt_AccountBalance_SearchStartDate"))
        )
        start_date.clear()
        time.sleep(0.5)  # Pequeña espera para evitar problemas de interacción
        start_date.send_keys(fecha_inicio)

        # Espera explícita para el campo de fecha de fin
        end_date = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "txt_AccountBalance_SearchEndDate"))
        )
        end_date.clear()
        time.sleep(0.5)  # Pequeña espera para evitar problemas de interacción
        end_date.send_keys(fecha_fin)

        # "Forzar" la actualización de la consulta con las fechas antes de cada descarga
        search_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btn_Search"))  # Ajusta el ID del botón de búsqueda si es necesario
        )
        driver.execute_script("arguments[0].click();", search_button)
        time.sleep(3)  # Espera para que la página se actualice con los datos correctos

        # Iterar sobre cada moneda y realizar la descarga
        for moneda, boton_id in monedas.items():
            print(f"Seleccionando la moneda: {moneda}...")
            currency_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, boton_id))
            )
            
            # Hacer clic en el botón de moneda
            driver.execute_script("arguments[0].click();", currency_button)
            time.sleep(2)  # Espera para que la moneda se cargue

            # Forzar una segunda actualización con las fechas seleccionadas
            print("Forzando actualización de la consulta con las fechas seleccionadas...")
            driver.execute_script("arguments[0].click();", search_button)
            time.sleep(3)

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
            new_file_name = f"{cliente_id}_{cliente_nombre}_CC_{moneda}_{fecha_inicio.replace('/', '')}_{fecha_fin.replace('/', '')}.xls"
            os.rename(latest_file, os.path.join(download_dir, new_file_name))
            print(f"Archivo renombrado a: {new_file_name}")

except Exception as e:
    print(f"Ocurrió un error durante el proceso: {e}")
    driver.save_screenshot('error_screenshot.png')  # Captura de pantalla en caso de error
    print("Captura de pantalla guardada como error_screenshot.png")

finally:
    driver.quit()
    print("Proceso completado")
