from selenium import webdriver
import time
import pywhatkit as kit

# Función para realizar scraping de una página web


def scrape_website(url):
    # Inicializar el WebDriver
    driver = webdriver.Chrome(
        '../TP-Programacion-Avanzada/chrome-win64/chrome.exe')
    driver.get(url)
    time.sleep(5)  # Espera a que la página se cargue completamente

    # Ejemplo: obtener el título de la página
    title = driver.find_element_by_xpath('//li[@data-aut-id="itemBox"]')
    driver.quit()
    return title

# Función para enviar un mensaje por WhatsApp


def send_whatsapp_message(phone_number, message):
    # Envía un mensaje de WhatsApp al número especificado a la hora actual + 1 minuto
    kit.sendwhatmsg(phone_number, message,
                    time.localtime().tm_hour, time.localtime().tm_min + 1)


# URL del sitio web que deseas hacer scraping
url = 'https://pypi.org/project/pywhatkit/'

# Scrapea la página web y obtiene el resultado
result = scrape_website(url)

# Envía el resultado scrapeado como un mensaje de WhatsApp
# Actualiza con el número de teléfono del contacto incluyendo el código del país
phone_number = "+541122595162"
send_whatsapp_message(phone_number, result)
