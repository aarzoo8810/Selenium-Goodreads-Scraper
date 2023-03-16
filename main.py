from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import time

FIREFOX_DRIVER_PATH = "/home/mushoku/developer/geckodriver"
GOODREADS_URL = "https://www.goodreads.com/book/show/22360832-is-it-wrong-to-try-to-pick-up-girls-in-a-dungeon-light-novels-vol-1"
SEARCH_KEYWORD = "light novel"

class GoodreadsScraper:
    def __init__(self):
        self.service = Service(FIREFOX_DRIVER_PATH)
        self.driver = webdriver.Firefox(service=self.service)
        print("opening browser")

    def search(self):
        self.driver.get(GOODREADS_URL)
        time.sleep(5)
        print(">>>Browser Opened")

        title = self.driver.find_element(by=By.TAG_NAME,
                                         value="h1").text
        print(f"{title = }")

        author_illustrator = self.driver.find_elements(By.CLASS_NAME,
                                          value="ContributorLink__name")
        author = author_illustrator[0].text
        illustrator = author_illustrator[1].text
        print(f"{author = }")
        print(f"{illustrator = }")
        
        description = self.driver.find_element(By.CLASS_NAME,
                                               value="Formatted").get_attribute("innerHTML")
        print(f"{description = }")
        
        genre_more_btn = self.driver.find_element(By.CLASS_NAME,
                                                  value="Button__container")
        genre_more_btn.click()
        
        genre_list = [genre.text for genre in self.driver.find_elements(By.CSS_SELECTOR,
                                               value="html body div#__next div.PageFrame.PageFrame--siteHeaderBanner main.PageFrame__main.BookPage div.BookPage__gridContainer div.BookPage__rightColumn div.BookPage__mainContent div.BookPageMetadataSection div.BookPageMetadataSection__genres ul.CollapsableList div.Button__container")]
        print(f"{genre_list = }")

ob = GoodreadsScraper()
ob.search()
