import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ============================
# CONFIGURACIÓN DEL NAVEGADOR
# ============================

options = Options()
options.add_argument("--headless")              # Necesario en GitHub Actions
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

# User-Agent compatible con Linux (GitHub Actions)
user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0"
options.set_preference("general.useragent.override", user_agent)

driver = webdriver.Firefox(options=options)


# ============================
# FUNCIONES
# ============================

def cargar_cookies(driver, archivo):
    """Cargar cookies desde un archivo JSON"""
    try:
        with open(archivo, "r", encoding="utf-8") as file:
            cookies = json.load(file)

        for cookie in cookies:
            # Firefox no acepta cookies con 'sameSite' inválido
            cookie.pop('sameSite', None)
            driver.add_cookie(cookie)

        
    except Exception as e:
        print("Error al cargar cookies:", e)


# ============================
# INICIO DEL SCRAPER
# ============================

# 1) Abrir X para cargar cookies

driver.get("https://x.com/home")
time.sleep(5)

# 2) Cargar cookies
cargar_cookies(driver, "cookies.json")

# 3) Refrescar para aplicar cookies
driver.refresh()
time.sleep(5)

# 4) Ir al tweet objetivo
url = "https://x.com/lynk0x/status/1874761902389375231"
driver.get(url)
time.sleep(5)

# 5) Scroll para cargar respuestas
print("Haciendo scroll...")
for _ in range(10):
    driver.execute_script("window.scrollBy(0, window.innerHeight);")
    time.sleep(1)

# 6) Esperar que aparezca el contenedor de tweets
try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "section.css-175oi2r"))
    )
except:
    print("No se encontró el section.css-175oi2r, continuando igual...")


# ============================
# EXTRAER NOMBRES Y TWEETS
# ============================

user_names = driver.find_elements(By.CSS_SELECTOR, '[data-testid="User-Name"]')
tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweetText"]')

max_length = min(len(user_names), len(tweets))



# ============================
# GUARDAR RESULTADOS EN TXT
# ============================

with open("tweets_guardados.txt", "w", encoding="utf-8") as file:
    for i in range(max_length):
        user_name = user_names[i].text
        tweet = tweets[i].text

        
        
        

        file.write(f"Usuario: {user_name}\n")
        file.write(f"Tweet: {tweet}\n")
        file.write("-" * 40 + "\n")



driver.quit()
