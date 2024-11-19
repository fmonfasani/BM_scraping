import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def obtener_cuentas(driver):
    """
    Scrapea la lista de cuentas de la página y las devuelve como una lista de diccionarios.
    """
    cuentas = []
    driver.get("https://bullmarketbrokers.com/Clients/AccountList")  # Cambia a la URL correcta

    # Esperar a que la lista de cuentas esté cargada
    cuentas_elementos = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".account-row"))  # Cambia al selector adecuado
    )

    # Extraer datos de cada cuenta
    for elemento in cuentas_elementos:
        try:
            account_id = elemento.get_attribute("data-id")
            account_text = elemento.find_element(By.CLASS_NAME, "account-text").text
            account_number = elemento.find_element(By.CLASS_NAME, "account-number").text

            cuentas.append({
                "id": int(account_id),
                "text": account_text,
                "number": int(account_number)
            })
        except Exception as e:
            print(f"Error al procesar una cuenta: {e}")

    return cuentas

def guardar_en_json(data, archivo):
    """
    Guarda los datos en un archivo JSON.
    """
    with open(archivo, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Configurar Selenium
chrome_options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=chrome_options)

try:
    # Iniciar sesión antes de scrapear
    print("Iniciando sesión...")
    driver.get("https://bullmarketbrokers.com/Security/SignIn")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "Email"))).send_keys("tu_email")
    driver.find_element(By.NAME, "Password").send_keys("tu_contraseña")
    driver.find_element(By.ID, "submitButton").click()

    # Scrapeo de cuentas
    print("Obteniendo lista de cuentas...")
    cuentas = obtener_cuentas(driver)
    print(f"Se obtuvieron {len(cuentas)} cuentas.")

    # Guardar en un archivo JSON
    archivo_salida = "clientes.json"
    guardar_en_json(cuentas, archivo_salida)
    print(f"Cuentas guardadas en el archivo {archivo_salida}.")

except Exception as e:
    print(f"Ocurrió un error: {e}")

finally:
    driver.quit()
