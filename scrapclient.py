from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuración del navegador
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

# Inicializar el driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # Abrir la página de inicio de sesión
    driver.get("https://bullmarketbrokers.com/Security/SignIn")
    
    # Esperar y llenar el campo de correo electrónico
    email_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "Email"))
    )
    email_field.send_keys("marcelolezcano_17@hotmail.com")
    
    # Esperar y llenar el campo de contraseña
    password_field = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "Password"))
    )
    password_field.send_keys("Inversiones24$")
    
    # Hacer clic en el botón de enviar
    submit_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "submitButton"))
    )
    submit_button.click()
    
    # Esperar a que la página cargue después del inicio de sesión
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    # Ejecutar un script JavaScript para obtener los datos de sessionStorage
    try:
        # Obtener todas las claves y valores de sessionStorage
        session_storage_data = driver.execute_script("""
            let storage = window.sessionStorage;
            let keys = Object.keys(storage);
            let data = {};
            for (let key of keys) {
                data[key] = storage.getItem(key);
            }
            return data;
        """)

        # Mostrar las claves y valores obtenidos
        print("Datos de sessionStorage:")
        for key, value in session_storage_data.items():
            print(f"Clave: {key} => Valor: {value}")

    except Exception as e:
        print(f"Error al obtener sessionStorage: {e}")

except Exception as e:
    print(f"Error encontrado: {e}")
    driver.save_screenshot("error_screenshot.png")
finally:
    # Cerrar el navegador
    driver.quit()
