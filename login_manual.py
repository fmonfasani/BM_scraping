from selenium import webdriver
import pickle
import os
import time

# Configura el perfil de Chrome
profile_path = r"C:\Users\fmonf\AppData\Local\Google\Chrome\User Data\Default"
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-data-dir={profile_path}")

# Inicia el navegador con el perfil especificado
driver = webdriver.Chrome(options=chrome_options)

# Accede a la página principal del sitio donde ya tienes la sesión iniciada
driver.get("https://bullmarketbrokers.com/Clients/accountbalance")
time.sleep(30)  # Espera para asegurarse de que la sesión esté cargada

# Guarda las cookies en un archivo
with open("cookies.pkl", "wb") as file:
    pickle.dump(driver.get_cookies(), file)

print("Cookies guardadas con éxito.")
driver.quit()
