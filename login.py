from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configura las opciones de Selenium para conectarse a la sesión de Chrome ya abierta
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9223")

# Inicia el navegador utilizando la sesión de depuración
driver = webdriver.Chrome(options=chrome_options)

# Ahora estás en la misma sesión de Chrome que tienes abierta manualmente y logueada
# Accede a la página de saldo directamente
driver.get("https://bullmarketbrokers.com/Clients/accountbalance")
time.sleep(5)

# Ejemplo de scraping: descarga o extrae datos de saldo
try:
    # Asegúrate de que el contenido esté cargado, luego haz tu scraping
    balance = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//elemento_xpath_para_saldo"))
    )
    print("Saldo encontrado:", balance.text)
except Exception as e:
    print("No se pudo encontrar el saldo:", e)

# Aquí puedes agregar más scraping si necesitas otros datos
# Por ejemplo, descarga archivos de Excel, etc.

driver.quit()
