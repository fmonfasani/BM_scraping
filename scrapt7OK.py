import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import getpass
from datetime import datetime

start_time = time.time()

# Configuración de descarga y opciones de Chrome
base_download_dir = os.path.join(os.getcwd(), "Descargas_PDFs")
if not os.path.exists(base_download_dir):
    os.makedirs(base_download_dir)

chrome_options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": base_download_dir,
    "download.prompt_for_download": False,
    "plugins.always_open_pdf_externally": True,
}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(120)

# Credenciales de inicio de sesión
email = "marcelolezcano_17@hotmail.com"
password = getpass.getpass("Ingresa tu contraseña: ")

# Lista de monedas y sus IDs de botón
monedas = {
    "PESOS": "btn_filter_pesos",
    "DÓLARES": "btn_filter_dolares",
    "DÓLARES CABLE": "btn_filter_dolares_cable"
}

# Lista de cuentas de usuario
stock_accounts = [
    {"id": 40756, "text": "LEZCANO JUAN MARCELO - Catalaxia SA", "number": 13641},
    {"id": 42222, "text": "Wichmann, Maria Alejandra", "number": 15154},
    {"id": 42223, "text": "Ramirez Julio Daniel", "number": 15155},
    {"id": 42509, "text": "Torres Cayman, Francisco Jose", "number": 18383},
    {"id": 42521, "text": "Torres, Silvia Mariana - Catalaxia S.A.", "number": 15380},
    {"id": 42522, "text": "Marino Dansey Martin Miguel", "number": 15381},
    {"id": 42528, "text": "Wilson, Eliane Grisel", "number": 15460},
    {"id": 42673, "text": "Ybarra, Juan Pablo", "number": 15595},
    {"id": 43088, "text": "Sosa Figueroa Silvio Federico", "number": 16057},
    {"id": 43324, "text": "Gomez Gigliani, Federico", "number": 16284},
    {"id": 43488, "text": "Nielsen Lucas Emilio", "number": 16469},
    {"id": 43552, "text": "Russo, Juan Pablo", "number": 16541},
    {"id": 43567, "text": "Torres, Santa Cruz", "number": 16545},
    {"id": 44522, "text": "Etchegaray Ana Lia", "number": 17516},
    {"id": 44690, "text": "Vara Alfredo", "number": 17695},
    {"id": 44691, "text": "Meuli Pablo Esteban Gabriel", "number": 17696},
    {"id": 45474, "text": "Jimenez Maria Alejandra", "number": 18481},
    {"id": 46407, "text": "Nazer Guillermo Gamal", "number": 19450},
    {"id": 46417, "text": "Ceroleni Alejandro Javier", "number": 19457},
    {"id": 47438, "text": "Perez Cornelia Abdona", "number": 20449},
    {"id": 52598, "text": "Romero Augusto", "number": 28328},
    {"id": 56525, "text": "Lezcano Yamil David", "number": 32248},
    {"id": 60593, "text": "González Oliver Adelaida Elsa", "number": 36427},
    {"id": 70462, "text": "PEREZ SERGIO ANTONIO", "number": 46761},
    {"id": 82395, "text": "Brescovich Elizabeth Romina", "number": 59502},
    {"id": 90260, "text": "VALLEJOS ANGEL GABRIEL", "number": 67356},
    {"id": 102817, "text": "Fernandez Ingrid Magali", "number": 79874},
    {"id": 114311, "text": "Gaona Evelin Yanet", "number": 91175},
    {"id": 117219, "text": "Obregon Almeida Fernando", "number": 94050},
    {"id": 124392, "text": "Franco Rodriguez Diego Jose", "number": 101376},
    {"id": 124587, "text": "Varela Diego Sebastian", "number": 101572},
    {"id": 124986, "text": "Lezcano Marcelo Antonio", "number": 101972},
    {"id": 127949, "text": "Ayala Marinich María Hortencia", "number": 104931},
    {"id": 127954, "text": "Pintos Nahuel Alejandro", "number": 104936},
    {"id": 128578, "text": "Rodríguez Mabel Agustina", "number": 105561},
    {"id": 131644, "text": "GUERRA JUAN ANTONIO", "number": 108602},
    {"id": 148053, "text": "Benitez Carlos Andres", "number": 124824},
    {"id": 156855, "text": "Costa Julio Cesar", "number": 133576},
    {"id": 158316, "text": "Milovich Juan Pablo", "number": 135005},
    {"id": 168517, "text": "Rujana Mariano Agustín", "number": 145107},
    {"id": 173935, "text": "Aranda Pedro Emmanuel", "number": 150428},
    {"id": 174938, "text": "Ramirez Gomez Mauro Adrian", "number": 151415},
    {"id": 177236, "text": "Vallejos Ramon Luciano", "number": 153690},
    {"id": 202361, "text": "Raffin Naiara", "number": 179805},
    {"id": 213186, "text": "Lucas Javier Toledo", "number": 190549},
    {"id": 229171, "text": "VELEZ OSPINA BAYRON AUGUSTO", "number": 206176},
    {"id": 230706, "text": "TINAZZIO BRONZUOLI JOSÉ ALBERTO", "number": 207697},
    {"id": 259880, "text": "TINAZZIO BRONZUOLI JOSÉ ALBERTO", "number": 155030},
    {"id": 263557, "text": "BENITEZ ROLLET SILVIA MELINA", "number": 247435},
    {"id": 278964, "text": "PEREZ VARGAS FLAVIA VANESA", "number": 262705},
    {"id": 304816, "text": "URIBE MARISA DEL VALLE", "number": 289070},
    {"id": 323578, "text": "TORRES PEDRO HERNAN", "number": 307900},
    {"id": 328156, "text": "ARCARO LEONEL ALEXIS", "number": 312512},
    {"id": 338951, "text": "SOSA MARIO LEANDRO", "number": 323389},
    {"id": 351768, "text": "RUJANA MARIO RUBEN", "number": 336279},
    {"id": 354132, "text": "OLIVERA MANSILLA RODRIGO EMMANUEL", "number": 338645},
    {"id": 355149, "text": "SILVA JUAN IGNACIO", "number": 339662},
    {"id": 355160, "text": "RAFART MARÍA ESTELA", "number": 339673},
    {"id": 358572, "text": "CUZZIOL GRACIELA RITA", "number": 343121},
    {"id": 360330, "text": "PUJALTE FACUNDO LUIS", "number": 344897},
    {"id": 360555, "text": "ZALAZAR RODRIGO EZEQUIEL ALBERTO", "number": 345125},
]

# Fechas para el reporte
fecha_inicio = "01/01/2024"
fecha_fin = "31/10/2024"
fecha_nombre = "Reporte_2024"  # para usar en el nombre del archivo

# Función para esperar hasta que el archivo esté completamente disponible
def esperar_descarga_completa(nombre_base, tiempo_espera=120):
    tiempo_inicial = time.time()
    while True:
        archivos_temporales = [
            f for f in os.listdir(base_download_dir)
            if f.startswith(nombre_base) and not f.endswith('.crdownload') and not f.endswith('.tmp')
        ]
        if archivos_temporales:
            latest_file = max([os.path.join(base_download_dir, f) for f in archivos_temporales], key=os.path.getctime)
            try:
                with open(latest_file, 'rb'):
                    return latest_file
            except (PermissionError, FileNotFoundError):
                pass

        if time.time() - tiempo_inicial > tiempo_espera:
            print(f"No se pudo acceder al archivo después de {tiempo_espera} segundos.")
            return None
        time.sleep(1)

try:
    print("Iniciando sesión...")
    driver.get("https://bullmarketbrokers.com/Security/SignIn")
    
    # Esperar y completar el formulario de inicio de sesión
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "Email"))).send_keys(email)
    driver.find_element(By.NAME, "Password").send_keys(password)
    driver.find_element(By.ID, "submitButton").click()
    time.sleep(10)  # Espera para la autenticación de dos factores si es necesario

    print("Accediendo a la página de balance...")
    driver.get("https://bullmarketbrokers.com/Clients/accountbalance")

    for account in stock_accounts:
        cliente_nombre = account["text"]
        cliente_number = account["number"]

        # Crear una carpeta específica para el usuario en `download_dir`
        user_download_dir = os.path.join(base_download_dir, f"{cliente_nombre.replace(' ', '_')}({cliente_number})")
        if not os.path.exists(user_download_dir):
            os.makedirs(user_download_dir)
        
        print(f"Seleccionando cuenta para el usuario {cliente_nombre}...")
        account_selector = WebDriverWait(driver, 60).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.select2-container a.select2-choice"))
        )
        
        # Hacer clic en el selector para abrir el menú desplegable
        account_selector.click()
        time.sleep(1)

        # Seleccionar la cuenta específica
        desired_account = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, f"//div[@class='select2-result-label' and contains(text(), '{cliente_number}')]"))
        )
        driver.execute_script("arguments[0].click();", desired_account)
        print(f"Usuario seleccionado: {cliente_number} {cliente_nombre}")
        
        # Cerrar el menú desplegable
        driver.find_element(By.CSS_SELECTOR, "body").click()
        time.sleep(1)

        # Configurar fechas de inicio y fin para el reporte
        print("Estableciendo las fechas de búsqueda...")
        start_date = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "txt_AccountBalance_SearchStartDate")))
        start_date.clear()
        start_date.send_keys(fecha_inicio)
        
        end_date = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "txt_AccountBalance_SearchEndDate")))
        end_date.clear()
        end_date.send_keys(fecha_fin)

        # Iniciar la búsqueda para cada moneda
        for moneda, boton_id in monedas.items():
            print(f"Seleccionando la moneda: {moneda}...")
            currency_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, boton_id)))
            driver.execute_script("arguments[0].click();", currency_button)
            time.sleep(2)

            print(f"Descargando archivo de Excel para {moneda}...")
            download_link = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Descargar Excel')]"))
            )
            download_link.click()

            latest_file = esperar_descarga_completa("Cuenta Corriente")

            if latest_file:
                new_file_name = f"{cliente_number}_{cliente_nombre.replace(' ', '_')}_CC_{moneda}_{fecha_nombre}.xls"
                os.rename(latest_file, os.path.join(user_download_dir, new_file_name))
                print(f"Archivo renombrado y movido a la carpeta: {new_file_name}")
            else:
                print(f"Error al renombrar el archivo para {moneda} en cuenta {cliente_nombre}.")

        time.sleep(3)  # Esperar un momento antes de pasar a la siguiente cuenta

except Exception as e:
    print(f"Ocurrió un error durante el proceso: {e}")
    driver.save_screenshot('error_screenshot.png')
    print("Captura de pantalla guardada como error_screenshot.png")

finally:
    driver.quit()
    print("Proceso completado")

    end_time = time.time()
    elapsed_time_minutes = (end_time - start_time) / 60
    elapsed_time = elapsed_time_minutes * 60
    print(f"Tiempo transcurrido: {elapsed_time_minutes:.2f} minutos")
    print(f"Tiempo total de ejecución: {elapsed_time:.2f} segundos")
