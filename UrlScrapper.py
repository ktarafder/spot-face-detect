import re
import os
import time
import aiohttp
import asyncio
import requests
from selenium import webdriver
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from concurrent.futures import ThreadPoolExecutor
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0"
}

def Progress_Bar(current, total, bar_length=20):
    fraction = current / total
    arrow = int(fraction * bar_length - 1) * '=' + '>'
    padding = (bar_length - len(arrow)) * ' '
    
    return f'Progress: [{arrow}{padding}] {int(fraction * 100)}%'

def Check_Dir():
    if not os.path.exists('./Profile_Images'):
        os.makedirs('./Profile_Images')

def normalize_name(name):
    name_parts = name.split()
    
    normalized_parts = [part.capitalize() for part in name_parts]
    
    return " ".join(normalized_parts)

def Extract_Camp_Dir_Image(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    try:
        name_element = driver.find_element(By.XPATH, "/html/body/main/div/div/div[1]/h4")
        name = normalize_name(name_element.text.strip())
    except NoSuchElementException:
        return
    
    try:
        image = driver.find_element(By.XPATH, "//img[@alt='PantherCard  Image']")
    except NoSuchElementException:
        return
    
    Check_Dir()
    
    img_url = image.get_attribute("src")
    
    img_data = requests.get(img_url).content
    
    filename = f"{name.replace(' ', '_')}.jpg"
    with open(f'./Profile_Images/{filename}', "wb") as handler:
        handler.write(img_data)
    
    print(f"Image saved as {filename}")

def Extract_Profile_Url(PageNum):
    Url=f"https://cas.gsu.edu/profile-directory/?wpv_view_count=13592-TCPID13610&wpv_paged={PageNum}"
    response = requests.get(Url,headers=headers).text
    
    pattern = r'href="(https://cas\.gsu\.edu/profile/[^"]+)"'

    return re.findall(pattern, response)

def Extract_Profile_Image(url):
    response = requests.get(url).text
    
    name_match = re.search(r'<meta property="og:title" content="([^"]+)"', response)
    image_match = re.search(r'<meta property="og:image" content="([^"]+)"', response)
    
    name = normalize_name(name_match.group(1))
    try:
        image_url = image_match.group(1)
    except:
        return
    
    Check_Dir()
    
    image_response = requests.get(image_url)
    if image_response.status_code == 200:

        file_extension = os.path.splitext(urlparse(image_url).path)[1]
        
        filename = ''.join(c for c in name if c.isalnum() or c in (' ', '.', '-')).rstrip()
        filename = filename.replace(' ', '_') + file_extension
        
        with open(f'./Profile_Images/{filename}', 'wb') as f:
            f.write(image_response.content)


def Professor_Scrapper():
    links = []

    for x in range(1,22):
        links = links + Extract_Profile_Url(x)
        os.system("cls")
        print(Progress_Bar(x, 21))
        print(f'Step {x} of 21')

    print("Links found completed!")

    time.sleep(2)
    os.system("cls")

    print("Cleaning Links")

    Cleaned_links = []
    for item in links:
        if item not in Cleaned_links:
            Cleaned_links.append(item)

    print ("Links Ready")
    time.sleep(2)
    os.system("cls")
    

    counter = 0
    link_length = len(Cleaned_links)
    for link in Cleaned_links:
        counter = counter + 1
        Extract_Profile_Image(link)
        os.system("cls")
        print(Progress_Bar(counter, link_length))
        print(f'Step {counter} of {link_length}')

def Student_Scrapper():
    driver = webdriver.Chrome()
    for x in range(10000000):
        driver.get(f"https://campusdirectory.gsu.edu/People?id=100000000{x:07d}")
        Extract_Camp_Dir_Image(driver)
        os.system("cls")
        print(Progress_Bar(x, 9999999))
        print(f'Step {x} of 9999999')

#Professor_Scrapper()
Student_Scrapper()

os.system("cls")
print("Images Captured")
