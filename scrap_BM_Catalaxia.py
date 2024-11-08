from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import getpass  # Para ocultar la contraseña al escribirla

# Solicita el usuario y la contraseña desde la consola
email = "marcelolezcano_17@hotmail.com"
password = getpass.getpass("Ingresa tu contraseña: ")

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

# Inicia el navegador
driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(120)  # Timeout general para cargas de página

try:
    # Navega a la página de inicio de sesión
    driver.get("https://bullmarketbrokers.com/Security/SignIn")
    time.sleep(2)

    # Busca e ingresa el usuario y la contraseña
    email_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "Email")))
    password_field = driver.find_element(By.NAME, "Password")
    email_field.send_keys(email)
    password_field.send_keys(password)

    # Clic en el botón de inicio de sesión
    submit_button = driver.find_element(By.ID, "submitButton")
    submit_button.click()
    time.sleep(15)  # Espera para segundo factor

    # Pausa para el código de autenticación manual
    #input("Ingresa el código de autenticación de dos factores y presiona Enter para continuar...")

    # Navega a la lista de usuarios
    driver.get("URL_DE_LA_SECCIÓN_DE_USUARIOS")  # Cambia esta URL según sea necesario
    time.sleep(3)

    # Encuentra el contenedor de usuarios
    users_container = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "select2-drop")))
    user_elements = users_container.find_elements(By.CSS_SELECTOR, "li.select2-result-selectable")

    # Lista de monedas para descargar
    currencies = ["PESOS", "DOLARES", "DOLARES CABLE"]

    # Recorre cada usuario
    for user_element in user_elements:
        user_text = user_element.find_element(By.CLASS_NAME, "select2-result-label").text
        user_id, user_name = user_text.split(" ", 1)
        print(f"Iniciando descarga para el usuario: {user_name} (ID: {user_id})")

        # Haz clic en el usuario para seleccionarlo
        driver.execute_script("arguments[0].click();", user_element)
        time.sleep(2)

        # Navega a la página de balance de cada usuario seleccionado
        driver.get("https://bullmarketbrokers.com/Clients/accountbalance")
        time.sleep(3)

        # Realiza las descargas de cada moneda para el usuario seleccionado
        for currency in currencies:
            try:
                # Haz clic en el botón de filtro de la moneda
                filter_button = WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.ID, f"btn_filter_{currency.lower().replace(' ', '_')}"))
                )
                driver.execute_script("arguments[0].click();", filter_button)
                time.sleep(3)

                # Haz clic en el botón de descarga de Excel
                download_excel_button = WebDriverWait(driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Descargar Excel')]"))
                )
                driver.execute_script("arguments[0].click();", download_excel_button)
                time.sleep(5)
                print(f"Descarga del archivo Excel en {currency} completada para el usuario {user_name}.")
            except Exception as e:
                print(f"Error al descargar el archivo Excel en {currency} para el usuario {user_name}: {e}")

        # Pausa entre usuarios para evitar problemas de sobrecarga
        time.sleep(10)

except Exception as e:
    print("Ocurrió un error durante el proceso:", e)

finally:
    # Cierra el navegador al finalizar
    
    print(f"Descargas completadas en la carpeta: {download_dir}")
