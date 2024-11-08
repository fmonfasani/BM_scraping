from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import getpass

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

driver = webdriver.Chrome(options=chrome_options)
driver.set_page_load_timeout(120)

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






# Información de divisas y cuentas (con todos los usuarios)
divisas = ["PESOS", "DOLARES", "DOLARES CABLE"]
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
    {"id": 361521, "text": "SILVA ARNALDO WILFRIDO", "number": 346093},
    {"id": 367594, "text": "VALLEJOS DIEGO MARTIN", "number": 352185},
    {"id": 369577, "text": "BALMACEDA JORGE BENJAMIN OSVALDO", "number": 354180},
    {"id": 372518, "text": "SAENZ CARINA NOEMI", "number": 357146},
    {"id": 372815, "text": "MENDIBURU JUAN JOSE", "number": 357445},
    {"id": 374275, "text": "RADKE LETICIA LIZ", "number": 358914},
    {"id": 378018, "text": "ALBES ANGEL OSCAR", "number": 362670},
    {"id": 378659, "text": "SEGOVIA RODRIGO IVAN", "number": 363322},
    {"id": 384054, "text": "TREPPO CATTANEO MONICA ALEJANDRA", "number": 368757},
    {"id": 384181, "text": "RIOS EDUARDO", "number": 368884},
    {"id": 386489, "text": "STECHINA DAHIANA ANELEY", "number": 371206},
    {"id": 391940, "text": "PELIZARDI OSCAR EDUARDO", "number": 155463},
    {"id": 392047, "text": "HAASE PABLO ANDRES", "number": 376801},
    {"id": 392520, "text": "VELEZ OSPINA BAYRON AUGUSTO", "number": 377270},
    {"id": 393118, "text": "VERON LILIAN ROSAURA", "number": 377866},
    {"id": 395300, "text": "ALTAMIRANO BARRENECHEA LUCILA ROSALIA", "number": 380045},
    {"id": 396517, "text": "DOMINGUEZ MACHADO MARIA ALEJANDRA", "number": 381259},
    {"id": 396790, "text": "RUIZ DIAZ JUAN PABLO", "number": 381531},
    {"id": 398239, "text": "ECHARRI MARIANA ALEJANDRA", "number": 382977},
    {"id": 399504, "text": "OCENTINK ÁNGEL JUAN", "number": 384235},
    {"id": 403657, "text": "ALVAREZ AUCAR SEBASTIAN GABRIEL", "number": 388372},
    {"id": 406391, "text": "CABRERA ALEJANDRA INES", "number": 397777},
    {"id": 409910, "text": "ALTA CALIDAD SRL", "number": 155538},
    {"id": 414187, "text": "VEGA GUSTAVO FABIAN", "number": 155550},
    {"id": 420354, "text": "GRIMBERG SANDRA CLARISSE", "number": 155580},
    {"id": 423679, "text": "YANDA MABEL GLADYS", "number": 414873},
    {"id": 428055, "text": "ARCARO WALTER ALEJANDRO", "number": 419247},
    {"id": 428142, "text": "JOSE MARÍA DE LOS ANGELES", "number": 419334},
    {"id": 433545, "text": "RODRIGUEZ VALLEJOS NOELIA AYMARA", "number": 900058},
    {"id": 433546, "text": "ARDUÑA JOSE LUIS", "number": 900059},
    {"id": 434359, "text": "ROLON LUCAS HERNAN", "number": 425545},
    {"id": 440180, "text": "LEZCANO GLORIA MARIEL", "number": 431348},
    {"id": 442848, "text": "BOGARIN MARTA EDITH", "number": 434023},
    {"id": 443079, "text": "NUÑEZ JUAN MANUEL", "number": 434251},
    {"id": 444696, "text": "RAMIREZ NORBERTO GABRIEL", "number": 435860},
    {"id": 445003, "text": "FISCHER GUILLERMO CARLOS", "number": 436164},
    {"id": 445099, "text": "VICENTE MARIA TERESA", "number": 436260},
    {"id": 450382, "text": "ALEGRE NESTOR FABIAN", "number": 441524},
    {"id": 451851, "text": "LINARES SILVIA DEL CARMEN", "number": 442983},
    {"id": 452431, "text": "CREMADES MARCOS", "number": 443561},
    {"id": 454579, "text": "MEZA MATIAS NICOLAS", "number": 900158},
    {"id": 458354, "text": "ROMANO JUAN MANUEL", "number": 900186},
    {"id": 459579, "text": "VELAZQUEZ ARIEL WALTER", "number": 450721},
    {"id": 464514, "text": "GOMEZ JOSE HERNAN", "number": 455646},
    {"id": 466267, "text": "GAITAN PEDRO LUIS", "number": 457392},
    {"id": 469482, "text": "MAIDANA MARTIN ALEJANDRO", "number": 460564},
    {"id": 472336, "text": "VEGA RAMON EUSEBIO", "number": 463402},
    {"id": 472781, "text": "SOSA ARIEL ALEJANDRO", "number": 463837},
    {"id": 472821, "text": "ROBLEDO DUARTE FATIMA VANINA", "number": 463877},
    {"id": 474627, "text": "BERNARDIS CLAUDIA GABRIELA", "number": 465662},
    {"id": 474950, "text": "RAMIREZ NOELIA ALEJANDRA", "number": 465979},
    {"id": 476492, "text": "SALDAÑA MARÍA BELEN", "number": 467542},
    {"id": 476994, "text": "MARTINEZ SOLIS EMANUEL MATIAS", "number": 468044},
    {"id": 477132, "text": "RODRIGUEZ VALLEJOS LUCIA AYELEN", "number": 900339},
    {"id": 480533, "text": "RAFFIN FERNANDO DANIEL", "number": 471785},
    {"id": 481267, "text": "GÓMEZ MARIELA VICTORIA", "number": 472601},
    {"id": 483156, "text": "LEZCANO JUAN MARCELO - Catalaxia SA", "number": 900422},
    {"id": 486496, "text": "IRALA JUAN ALBERTO", "number": 478057},
    {"id": 486658, "text": "PARED JULIO CESAR", "number": 478249},
    {"id": 487173, "text": "GONZALEZ MARCELO ALEJANDRO", "number": 478823},
    {"id": 488531, "text": "ALMIRON MARISOL ESTEFANIA", "number": 480314},
    {"id": 491711, "text": "ESCOBAR LUIS ALBERTO", "number": 483757},
    {"id": 493466, "text": "ZAMPA YLDA LUCIA", "number": 900516},
    {"id": 493968, "text": "MAURICE GASTON FEDERICO", "number": 486107},
    {"id": 494506, "text": "SUAREZ ANALIA VERONICA", "number": 486650},
    {"id": 494519, "text": "PEREZ MARIA ISABEL", "number": 486663},
    {"id": 494801, "text": "MARINICH ROSA HORTENCIA", "number": 486952},
    {"id": 495426, "text": "MAURIÑO EDUARDO ALFREDO", "number": 487598},
    {"id": 496511, "text": "QUIROZ FERRARI LUIS ERNESTO", "number": 488735},
    {"id": 496514, "text": "SARTORI CARINA CECILIA", "number": 488738},
    {"id": 497126, "text": "HUGO DAVID DELLAMEA", "number": 489348},
    {"id": 499583, "text": "BENITEZ ROLLET SILVIA MELINA", "number": 900568},
    {"id": 500839, "text": "VALDEZ MARIELA ALEJANDRA", "number": 493209},
    {"id": 501920, "text": "SOSA PAULA LUCIA", "number": 494348},
    {"id": 503460, "text": "MEDINA MARIA ELENA", "number": 495888},
    {"id": 503623, "text": "BRITO FABIÁN ALEJANDRO", "number": 496054},
    {"id": 505239, "text": "SALINAS ALEJANDRO FABIO", "number": 497682},
    {"id": 505538, "text": "LEVATTI JORGE MARCELO", "number": 497967},
    {"id": 507247, "text": "RADZANOWICZ FEDERICO", "number": 499649},
    {"id": 507334, "text": "AVILA OMAR ENRIQUE", "number": 499736},
    {"id": 507836, "text": "MARTINEZ SOLIS EMANUEL MATIAS", "number": 900655},
    {"id": 508939, "text": "ROMERO PABLO LUIS", "number": 501213},
    {"id": 509021, "text": "VERNAL MARIANA ITATI", "number": 501291},
    {"id": 513662, "text": "PANIAGUA CARLOS ALBERTO", "number": 505840},
    {"id": 515329, "text": "PARED ALFREDO JAVIER", "number": 507466}
]
try:
    # Solicitar credenciales de administrador
    email = "marcelolezcano_17@hotmail.com"
    password = getpass.getpass("Ingresa tu contraseña: ")

    # Iniciar sesión en Bull Market
    driver.get("https://bullmarketbrokers.com/Security/SignIn")
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.NAME, "Email"))).send_keys(email)
    driver.find_element(By.NAME, "Password").send_keys(password)
    driver.find_element(By.ID, "submitButton").click()
    time.sleep(10)  # Espera para la autenticación en dos pasos si es necesario

    # Iterar sobre cada cuenta de usuario
    for account in stock_accounts:
        try:
            # Esperar hasta que el botón de cuenta esté presente y sea visible
            account_button = WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.XPATH, f"//button[@data-account-id='{account['number']}']"))
            )
            account_button.click()
            time.sleep(3)  # Esperar a que la página se actualice

            # Navegar a la página de balance
            driver.get("https://bullmarketbrokers.com/Clients/accountbalance")
            time.sleep(5)

            # Descargar archivos para cada divisa
            for divisa in divisas:
                try:
                    # Seleccionar el filtro de la divisa
                    filter_button = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.ID, f"btn_filter_{divisa.lower().replace(' ', '_')}"))
                    )
                    filter_button.click()
                    time.sleep(3)

                    # Descargar el archivo Excel
                    download_button = WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Descargar Excel')]"))
                    )
                    download_button.click()
                    time.sleep(5)  # Espera para asegurarse de que la descarga esté completa
                    print(f"Descarga completada para {divisa} en cuenta {account['text']}")
                except Exception as e:
                    print(f"Error descargando {divisa} para cuenta {account['text']}: {e}")

            # Espera antes de pasar a la siguiente cuenta
            time.sleep(3)

        except Exception as account_error:
            print(f"Error al seleccionar la cuenta {account['text']}: {account_error}")

except Exception as e:
    print("Ocurrió un error durante el proceso:", e)

finally:
    driver.quit()
    print("Proceso completado")