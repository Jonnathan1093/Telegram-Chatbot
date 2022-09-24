from selenium import webdriver # driver de selenium
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth # Ayuda a evitar que las webs nos detecten que somos un bot
from shutil import which

def iniciar_webdriver(headless=True):# Arranca webdriver con Chrome y lo devuelve 
    options = Options()
    if headless:
        options.add_argument("--headless") # para ejecutar chromedriver, pero sin abrir la ventana
    options.add_argument("--window-size=1000,1000") # Configurar dimension ventana alto y ancho
    options.add_argument("--start-maximized") # para maximizar la ventana 
    options.add_argument("--disable-dev-shm-usage") # Importante para usar en Heroku | Para usar un directorio temporal para crear archivos anonimos de memoria copartida
    options.add_argument("--disable-blink-features=AutomationControlled") # Para que el navigator.webdriver sea falso
    options.add_argument("--log-level=3") # Para que no muestre nada en la terminal
    lista = [
        "enable-automation", # Para ocultar "Un software automatizado de pruebas esta controlando chrome"
        "enable-logging", # Para ocultar Devtools
        ]
    options.add_experimental_option("excludeSwitches", lista)
    s = Service(which("chromedriver"))
    driver = webdriver.Chrome(service=s, options=options) #añadimos el argumento Options
    stealth(
        driver,
        languages=["es-ES", "es"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,)
    return driver
