import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

class WebScraper():
    def __init__(self):
        # Configure Chrome options
        options = webdriver.ChromeOptions()
        #options.add_argument("--headless")  # Facultatif : pour lancer Chrome en arrière-plan

        # Start chrome with webdriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # URL for each promotion to webscrap
        url_et3 = ('https://ade-planning.polytech.universite-paris-saclay.fr/direct/?data=95e000515dff41bf090dab728096f2e573fcc9d06b8b96dc3d93d2cb352384cbace4f64bd408b45ca39029774ea4690830bd1419659aefba2515ad45d7d6b2e60a177ea3fca78ebb8d09fcc527c2eb35c5c1eac4c431ea42a7b539b6ae09851fc8a517a39539834b65d418562645b25f6bed5e6629c39c1c84424e4705c803ab,1')

        url_promo = [url_et3]

        vacation_weeks = [1]

        #On navigue pour trouver les emplois du temps des ET3
        for url in url_promo:
            #Navigate through the promo calendar
            driver.get(url)
            time.sleep(random.uniform(3.47, 5.91))

            for week in range(15, 20): #ends the 48th week
                if week not in vacation_weeks:
                    xpath_week = ('/html/body/div[1]/div/div[2]/div[1]/div[3]/div/div/div[2]/div/div/div[1]/div/div/table['
                                  + str(week) + ']/tbody/tr[2]/td[2]/em/button')
                    button = driver.find_element(By.XPATH, xpath_week)
                    button.click()
                    time.sleep(random.uniform(3.33, 10.75))

                    #Download html pages in the right directory
                    with open('et3_html/' + str(week) + '.html', 'w', encoding="utf-8") as f:
                        f.write(driver.page_source)
        driver.quit()

#webscraper = WebScraper()