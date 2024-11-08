import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass

# Configuración de descarga y opciones de Chrome
download_dir = os.path.join(os.getcwd(), "Descargas")
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

# Lista de usuarios a descargar
usuarios = [
    {"id": 40756, "text": "LEZCANO JUAN MARCELO - Catalaxia SA", "number": "13641"},
    {"id": 42222, "text": "Wichmann, Maria Alejandra", "number": "15154"}
]

# Lista de monedas y sus IDs de botón
monedas = {
    "PESOS": "btn_filter_pesos",
    "DÓLARES": "btn_filter_dolares",
    "DÓLARES CABLE": "btn_filter_dolares_cable"
}

# Credenciales de inicio de sesión
email = "marcelolezcano_17@hotmail.com"
password = getpass.getpass("Ingresa tu contraseña: ")

# Función para esperar a que el archivo esté disponible y desbloqueado
def esperar_archivo_disponible(filepath, timeout=120):
    tiempo_inicial = time.time()
    while time.time() - tiempo_inicial < timeout:
        if os.path.exists(filepath) and not any(filepath.endswith(ext) for ext in ['.crdownload', '.tmp']):
            try:
                with open(filepath, 'rb'):
                    return True
            except PermissionError:
                time.sleep(1)
    return False

try:
    print("Iniciando sesión...")
    driver.get("https://bullmarketbrokers.com/Security/SignIn")
    
    # Esperar y completar el formulario de inicio de sesión
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "Email"))).send_keys(email)
    driver.find_element(By.NAME, "Password").send_keys(password)
    driver.find_element(By.ID, "submitButton").click()
    
    print("Esperando a que se cargue la página principal...")
    WebDriverWait(driver, 10).until(EC.url_changes("https://bullmarketbrokers.com/Security/SignIn"))

    print("Accediendo a la página de balance...")
    driver.get("https://bullmarketbrokers.com/Clients/accountbalance")

    for usuario in usuarios:
        cliente_text = usuario["text"]
        cliente_number = usuario["number"]

        print(f"Seleccionando cuenta para el usuario {cliente_text}...")
        account_selector = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.select2-container a.select2-choice"))
        )
        
        account_selector.click()
        time.sleep(1)

        desired_account = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@class='select2-result-label' and contains(text(), '{cliente_number}')]"))
        )
        driver.execute_script("arguments[0].click();", desired_account)
        print(f"Usuario seleccionado: {cliente_number} {cliente_text}")
        
        driver.find_element(By.CSS_SELECTOR, "body").click()
        time.sleep(1)

        for moneda, boton_id in monedas.items():
            print(f"Seleccionando la moneda: {moneda}...")
            currency_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, boton_id))
            )
            driver.execute_script("arguments[0].click();", currency_button)
            time.sleep(2)

            print(f"Descargando archivo de Excel para {moneda}...")
            download_link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Descargar Excel')]"))
            )
            download_link.click()
            
            # Esperar hasta que la descarga finalice y el archivo esté desbloqueado
            latest_file = max([os.path.join(download_dir, f) for f in os.listdir(download_dir)], key=os.path.getctime)
            if esperar_archivo_disponible(latest_file):
                new_file_name = f"{cliente_number}_{cliente_text.replace(' ', '_')}_CC_{moneda}_COMPLETO.xls"
                os.rename(latest_file, os.path.join(download_dir, new_file_name))
                print(f"Archivo renombrado a: {new_file_name}")
            else:
                print(f"Error: no se pudo renombrar el archivo para {cliente_text} - {moneda} después de {timeout} segundos.")

except Exception as e:
    print(f"Ocurrió un error durante el proceso: {e}")
    driver.save_screenshot('error_screenshot.png')
    print("Captura de pantalla guardada como error_screenshot.png")

finally:
    driver.quit()
    print("Proceso completado")
