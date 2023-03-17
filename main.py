#!/home/mushoku/developer/day-81-100-portofolio-project/day-92-goodreads-scraper/venv/bin/python

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
        time.sleep(10)
        print(">>>Browser Opened\n\n\n")
        if "sign_up" in self.driver.current_url:
            self.driver.back()

        title = self.driver.find_element(by=By.TAG_NAME,
                                         value="h1").text
        print(f"{title = }")

        poster_img_div = self.driver.find_element(
            by=By.CLASS_NAME, value="BookCover")
        poster_img_url = poster_img_div.find_element(
            By.CLASS_NAME, "ResponsiveImage").get_attribute("src")
        print(f"{poster_img_url = }")

        contributors = self.driver.find_element(By.CLASS_NAME,
                                                value="ContributorLinksList").text.replace("\n ", "").replace("\n", "")
        print(f"{contributors = }")

        description = self.driver.find_element(
            By.CLASS_NAME, value="Formatted").get_attribute("innerHTML")

        print(f"{description = }")

        genre_more_btn = self.driver.find_element(By.CSS_SELECTOR,
                                                  value="html body div#__next div.PageFrame.PageFrame--siteHeaderBanner main.PageFrame__main.BookPage div.BookPage__gridContainer div.BookPage__rightColumn div.BookPage__mainContent div.BookPageMetadataSection div.BookPageMetadataSection__genres ul.CollapsableList div.Button__container")
        genre_more_btn.click()

        genre_list = [genre.text for genre in self.driver.find_elements
                      (By.CLASS_NAME, value="BookPageMetadataSection__genreButton")]

        print(f"{genre_list = }")

        num_of_pages = self.driver.find_element(By.CSS_SELECTOR,
                                                value=".FeaturedDetails > p:nth-child(1)").text
        print(f"{num_of_pages = }")


ob = GoodreadsScraper()
ob.search()
