from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Ruta del perfil de usuario en Chrome donde tienes la sesión activa
profile_path = r"C:\Users\fmonf\AppData\Local\Google\Chrome\User Data\Default" 

# Configuración de ChromeOptions para usar el perfil existente
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={profile_path}")  # Ruta del perfil de usuario
chrome_options.add_argument("--remote-debugging-port=9222")  # Conexión a la sesión existente

# Inicia el navegador usando el perfil especificado
driver = webdriver.Chrome(options=chrome_options)

# Ve a la página de saldo de Bull Market (deberías estar ya logueado)
driver.get("https://bullmarketbrokers.com/Clients/accountbalance")
time.sleep(5)

# Directorio para guardar descargas
download_dir = os.path.join(os.getcwd(), "Descargas_PDFs")
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# Ejemplo de scraping: Descargar archivos de Excel en diferentes monedas
currencies = ["PESOS", "DOLARES", "DOLARES CABLE"]

for currency in currencies:
    try:
        # Selecciona el botón de filtro para la moneda deseada
        filter_button = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, f"btn_filter_{currency.lower().replace(' ', '_')}"))
        )
        driver.execute_script("arguments[0].click();", filter_button)
        time.sleep(3)

        # Haz clic en el botón de descarga de Excel
        download_excel_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Descargar Excel')]"))
        )
        driver.execute_script("arguments[0].click();", download_excel_button)
        time.sleep(5)
        print(f"Descarga del archivo Excel en {currency} completada.")
    except Exception as e:
        print(f"Error al descargar el archivo Excel en {currency}: {e}")

# Cierra el navegador
driver.quit()
print(f"Descargas completadas en la carpeta: {download_dir}")
