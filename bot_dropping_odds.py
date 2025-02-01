import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Bot
from concurrent.futures import ThreadPoolExecutor

# Configuration Telegram
TELEGRAM_TOKEN = "7765993140:AAFyd8E_39wXberEosiWqES_QwgyBschw6A"
TELEGRAM_CHAT_ID = "7663981935"

bot = Bot(token=TELEGRAM_TOKEN)

# Configuration Selenium
options = Options()
options.add_argument("--headless")  # Exécute Chrome sans interface graphique
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# URL de Dropping Odds
BASE_URL = "http://www.dropping-odds.com/live"

def envoyer_alerte(message):
    """Envoie une alerte sur Telegram."""
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def analyser_match(match_url):
    """Analyse un match spécifique pour détecter un drop > 0.99"""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(match_url)
    time.sleep(2)

    soup_match = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()  # Fermer le navigateur après analyse

    total_section = soup_match.find("div", string="Total")
    if total_section:
        table = total_section.find_next("table")
        rows = table.find_all("tr")

        for row in rows:
            cols = row.find_all("td")
            if len(cols) > 1:
                drop_value = cols[-1].text.strip().replace(",", ".")

                try:
                    drop_value = float(drop_value)
                    if drop_value > 0.99:
                        message = f"📢 ALERTE : Cote Drop élevée ({drop_value}) sur {match_url}"
                        envoyer_alerte(message)
                except ValueError:
                    continue  # Ignorer les erreurs de conversion

def scraper_dropping_odds():
    """Récupère la liste des matchs en live et les analyse en parallèle."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(BASE_URL)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    matchs = soup.select("tr.match-row a[href^='/match']")
    match_urls = ["http://www.dropping-odds.com" + match["href"] for match in matchs]
    import time

while True:
    time.sleep(60)  # Attendre 60 secondes avant de continuer (évite les erreurs de port)

