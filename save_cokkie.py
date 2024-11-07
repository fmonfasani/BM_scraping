from selenium import webdriver

# Configura Selenium y el perfil de Chrome si es necesario
chrome_options = webdriver.ChromeOptions()
# Agrega tu configuración de perfil aquí, si es necesaria
driver = webdriver.Chrome(options=chrome_options)

# Abre la página para establecer las cookies
driver.get("https://bullmarketbrokers.com")  # URL del sitio donde deseas agregar las cookies

# Cadena de cookies extraídas de document.cookie
cookie_string = "_gcl_aw=GCL.1730477169.CjwKCAjw-JG5BhBZEiwAt7JR68nayuo4lobRhChQGbHRqC_Q-10QrzDnqQD_SyBpdcqOgZCK3GWCshoCqeoQAvD_BwE; _gcl_gs=2.1.k1$i1730477167; _gac_UA-17836200-1=1.1730477169.CjwKCAjw-JG5BhBZEiwAt7JR68nayuo4lobRhChQGbHRqC_Q-10QrzDnqQD_SyBpdcqOgZCK3GWCshoCqeoQAvD_BwE; _gid=GA1.2.1038262470.1730890842; _gat=1; _ga_Q23PLCSDHW=GS1.1.1730900432.11.1.1730905308.0.0.0; _ga=GA1.1.987066544.1730126583; _ga_48G26YS1HB=GS1.2.1730900433.8.1.1730905308.58.0.0"

# Convierte el string de cookies en un diccionario para Selenium
cookies = cookie_string.split('; ')
for cookie in cookies:
    name, value = cookie.split('=', 1)
    cookie_dict = {
        'name': name,
        'value': value,
        'domain': 'bullmarketbrokers.com',  # Asegúrate de que el dominio coincida con el sitio
        'path': '/',
    }
    driver.add_cookie(cookie_dict)

# Refresca la página para aplicar las cookies
driver.refresh()

print("Cookies agregadas exitosamente.")
# Ahora puedes continuar con el script que requiere la sesión
