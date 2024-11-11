scraptClients.py
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import getpass

# Configuración del navegador
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)

# Credenciales de inicio de sesión
email = "marcelolezcano_17@hotmail.com"
password = getpass.getpass("Ingresa tu contraseña: ")

# Lista para almacenar la información de los clientes
clientes = []

try:
    print("Iniciando sesión...")
    driver.get("https://bullmarketbrokers.com/Security/SignIn")

    # Esperar y completar el formulario de inicio de sesión
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "Email"))).send_keys(email)
    driver.find_element(By.NAME, "Password").send_keys(password)
    driver.find_element(By.ID, "submitButton").click()
    time.sleep(10)  # Esperar para autenticación de dos factores, si es necesario

    print("Accediendo a la página de balance...")
    driver.get("https://bullmarketbrokers.com/Clients/accountbalance")

    # Seleccionar el menú de cuentas y extraer la lista de clientes
    account_selector = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.select2-container a.select2-choice"))
    )
    account_selector.click()
    time.sleep(2)

    # Obtener todos los elementos de la lista de cuentas
    account_elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='select2-result-label']"))
    )

    for element in account_elements:
        # Extraer el texto de cada cuenta y separar ID y nombre del cliente
        account_text = element.text
        parts = account_text.split(" - ")
        if len(parts) == 2:
            cliente_name = parts[0].strip()
            cliente_id = parts[1].strip()
            clientes.append({"name": cliente_name, "id": cliente_id})

    # Guardar la lista de clientes en un archivo JSON
    with open("clientes.json", "w") as file:
        json.dump(clientes, file, indent=4)

    print("Información de los clientes guardada en clientes.json")

except Exception as e:
    print(f"Ocurrió un error durante el proceso: {e}")
    driver.save_screenshot('error_screenshot.png')
    print("Captura de pantalla guardada como error_screenshot.png")

finally:
    driver.quit()
    print("Proceso completado")
