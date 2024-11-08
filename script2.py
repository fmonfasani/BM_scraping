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
#chrome_options.add_argument("--headless")  # Cambia a `--no-sandbox` si es necesario
driver = webdriver.Chrome(options=chrome_options)

# Iniciar sesión
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
    
    # Aumentar tiempo de espera y esperar que el elemento sea interactuable
    print("Esperando el selector de cuentas...")
    account_selector = WebDriverWait(driver, 180).until(  # Aumentar el tiempo de espera
        EC.visibility_of_element_located((By.CLASS_NAME, "select2-input"))
    )
    
    # Intenta hacer clic en el selector de cuentas
    print("Haciendo clic en el selector de cuentas...")
    account_selector.click()

    # Espera un momento para asegurar que la lista de cuentas aparezca
    time.sleep(2)

    # Intentar encontrar el usuario específico
    print("Buscando usuario específico...")
    desired_account = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@class='select2-result-label' and contains(text(), 'LEZCANO JUAN MARCELO - Catalaxia SA')]"))
    )
    
    # Si no se puede hacer clic, usar JavaScript
    driver.execute_script("arguments[0].click();", desired_account)

    print("Usuario seleccionado: LEZCANO JUAN MARCELO - Catalaxia SA")
    
    # Selección de la moneda
    print("Seleccionando la moneda...")
    currency_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "btn_filter_pesos"))  # Cambia a "btn_filter_dolares" o "btn_filter_dolares_cable" si es necesario
    )
    
    # Hacer clic en el botón de moneda
    driver.execute_script("arguments[0].click();", currency_button)

    # Espera adicional para asegurar que la selección se procese
    time.sleep(1)

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
    print("Descargando archivo de Excel...")
    download_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Descargar Excel')]")
    download_link.click()

    # Espera para asegurar la descarga del archivo
    time.sleep(5)

except Exception as e:
    print(f"Ocurrió un error durante el proceso: {e}")
    driver.save_screenshot('error_screenshot.png')  # Captura de pantalla en caso de error
    print("Captura de pantalla guardada como error_screenshot.png")

finally:
    driver.quit()
    print("Proceso completado")
