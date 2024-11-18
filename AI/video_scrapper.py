import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import time

# Read movie indexes from CSV
df = pd.read_csv('ai/merge_stats.csv')
movie_indexes = df.sort_values('rating_count', ascending=False)['movieId'].tolist() 

# Path to the ChromeDriver executable
service = Service(r"AI\chromedriver.exe")

def fix_imdb_ids(movie_id):
    if len(movie_id) < 7:
        fixed_id = movie_id.zfill(7)
    else:
        fixed_id = movie_id
        
    fixed_id = f"tt{fixed_id}"
    return fixed_id

def get_video(imdbId):
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument(r"user-data-dir=C:\Users\ASUS\AppData\Local\Google\Chrome\User Data")
    options.add_argument(r"profile-directory=Default")
    driver = webdriver.Chrome(service=service, options=options)
    fixed_id = fix_imdb_ids(imdbId)
    imdb_url = f"https://www.imdb.com/title/{fixed_id}/videogallery/"
    driver.get(imdb_url)
    wait = WebDriverWait(driver, 20)  # Increase wait time
    waiter = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ipc-slate-card:nth-child(1) > div:nth-child(1) > a:nth-child(2) > div:nth-child(2)')))
    elements = driver.find_elements(By.CSS_SELECTOR, 'div.ipc-slate-card')

    try:
        for i in range(1, len(elements) + 1):
            vid_type_element = driver.find_element(By.CSS_SELECTOR, f'div.ipc-slate-card:nth-child({i}) > div:nth-child(1) > a:nth-child(2) > div:nth-child(3) > span:nth-child(2)')
            vid_type = vid_type_element.text
            if 'trailer' in vid_type.lower():
                element = driver.find_element(By.CSS_SELECTOR, f'div.ipc-slate-card:nth-child({i}) > div:nth-child(1) > a:nth-child(2)')
                vid_link = element.get_attribute('href')
                break
    except Exception as e:
        raise Exception

    try:
        driver.get(vid_link)
        waiter = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.jw-video')))
        time.sleep(5)  # Add delay to ensure the video source is loaded
        vid_element = driver.find_element(By.CSS_SELECTOR, '.jw-video')
        vid_src = vid_element.get_attribute('src')

        return vid_src
    except Exception as e:
        raise Exception


