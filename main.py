from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


class GoodreadsScraper:
    def __init__(self):
        self.driver_path = "/home/mushoku/developer/geckodriver"
        self.base_url = "https://www.goodreads.com/"
        self.shelf_url = "https://www.goodreads.com/shelf/show/light-novel"
        self.genre = "Light Novel"
        self.language = "English"
        self.service = Service(self.driver_path)
        self.driver = webdriver.Firefox(service=self.service)
        self.url_book_list = []
        self.url_limit = 55

        print("opening browser")
        self.scrape_book_links()

    def scrape_book_links(self):
        """This function scrapes all links of book in book shelf page"""
        self.driver.get(self.shelf_url)
        book_url_tags = self.driver.find_elements(
            By.CLASS_NAME, value="bookTitle")

        self.book_url_list = [url_tag.get_attribute(
            "href") for url_tag in book_url_tags]
        self.scrape_books()

    def scrape_books(self):
        """This function takes list of book urls"""
        for book_url in self.book_url_list:
            print("Going to url ", book_url)
            self.driver.get(book_url)

            if "sign_up" in self.driver.current_url:
                self.driver.back()

            try:
                sign_up_popup = self.driver.find_element(
                    By.CSS_SELECTOR, ".Overlay__close > div:nth-child(1) > button:nth-child(1)")
            except NoSuchElementException:
                pass
            else:
                sign_up_popup.click()

            # this time.sleep is used for giving time to load data after popup
            time.sleep(5)
            genre_more_btn = self.driver.find_element(By.CSS_SELECTOR,
                                                      value="html body div#__next div.PageFrame.PageFrame--siteHeaderBanner main.PageFrame__main.BookPage div.BookPage__gridContainer div.BookPage__rightColumn div.BookPage__mainContent div.BookPageMetadataSection div.BookPageMetadataSection__genres ul.CollapsableList div.Button__container")
            genre_more_btn.click()

            genre_list = [genre.text for genre in self.driver.find_elements(
                By.CLASS_NAME, value="BookPageMetadataSection__genreButton")]
            print(f"{genre_list = }")

            if self.genre in genre_list:
                book_details_btn = self.driver.find_element(
                    By.CSS_SELECTOR, value="div.CollapsableList > div:nth-child(3)")
                book_details_btn.click()

                # some books don't have either isbn or language
                try:
                    # if isbn is not present then this line will give language
                    isbn = self.driver.find_element(
                        By.XPATH, "/html/body/div[1]/div/main/div[1]/div[2]/div[1]/div[2]/div[6]/div/span[2]/div[1]/span/div/dl/div[3]").text.strip()
                except NoSuchElementException:
                    isbn = None
                    language = None
                else:
                    if "Language" in isbn:
                        language = isbn.split("Language\n")[-1]
                        isbn = None
                    else:
                        isbn = isbn.split("ISBN\n")[-1]
                        language = self.driver.find_element(
                            By.CSS_SELECTOR, "div.DescListItem:nth-child(4) > dd:nth-child(2) > div:nth-child(1) > div:nth-child(1)").text.strip()
                
                book_items = []
                if language == self.language:
                    title = self.driver.find_element(
                        by=By.TAG_NAME, value="h1").text

                    book_cover_div = self.driver.find_element(
                        by=By.CLASS_NAME, value="BookCover")
                    book_cover_url = book_cover_div.find_element(
                        By.CLASS_NAME, "ResponsiveImage").get_attribute("src")

                    contributors = self.driver.find_element(
                        By.CLASS_NAME, value="ContributorLinksList").text.replace("\n ", "").replace("\n", "")

                    description = self.driver.find_element(
                        By.CLASS_NAME, value="Formatted").get_attribute("innerHTML")

                    page_edition = self.driver.find_element(
                        By.CSS_SELECTOR, value=".FeaturedDetails > p:nth-child(1)").text

                    num_of_pages = None
                    edition = page_edition
                    if "pages" in page_edition:
                        num_of_pages, edition = page_edition.split(" pages, ")

                    if num_of_pages:
                        num_of_pages = int(num_of_pages)

                    published_date = self.driver.find_element(
                        By.CSS_SELECTOR, value=".FeaturedDetails > p:nth-child(2)").text.split("published ")[-1]

                    recommended_book_section = self.driver.find_element(
                        By.CSS_SELECTOR, ".BookPage__relatedTopContent > div:nth-child(1) > div:nth-child(1) > section:nth-child(1) > div:nth-child(2) > div:nth-child(1)")

                    recommended_book_urls = [anchor_tag.get_attribute(
                        "href") for anchor_tag in recommended_book_section.find_elements(By.TAG_NAME, "a")]
                    
                    for url in recommended_book_urls:
                        if url not in self.url_book_list and len(self.url_book_list) < self.url_limit:
                            self.url_book_list.append(url)
                            print(len(self.url_book_list))
                            
                    
                    book_item = {"title": title,
                                 "book_cover_url": book_cover_url,
                                 "contributors": contributors,
                                 "genre": genre_list,
                                 "description": description,
                                 "num_of_pages": num_of_pages,
                                 "edition": edition,
                                 "isbn": isbn,
                                 "language": language,
                                 "published_date": published_date,
                                 }
                    book_items.append(book_item)
                    print(book_items)


ob = GoodreadsScraper()
