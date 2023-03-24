from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import pandas

driver_path = "/home/mushoku/developer/geckodriver"
base_url = "https://www.goodreads.com/"
shelf_url = "https://www.goodreads.com/shelf/show/light-novel"
url_limit = 5



def scrape_book_links():
    """This function scrapes book details and returns as list of dictionaries of book details"""
    genre = "Light Novel"
    desired_language = "English"
    
    print(">> opening browser....")
    service = Service(driver_path)
    driver = webdriver.Firefox(service=service)
    driver.get(shelf_url)
    
    book_url_tags = driver.find_elements(
        By.CLASS_NAME, value="bookTitle")
    
    book_url_list = [url_tag.get_attribute(
        "href") for url_tag in book_url_tags]
    
    book_items = []
    for book_url in book_url_list:
        if book_url_list.index(book_url) > url_limit:
            driver.quit()
        else:
            print("Making request to url:  ", book_url)
            driver.get(book_url)

            if "sign_up" in driver.current_url:
                driver.back()
            try:
                sign_up_popup = driver.find_element(
                    By.CSS_SELECTOR, ".Overlay__close > div:nth-child(1) > button:nth-child(1)")
            except NoSuchElementException:
                pass
            else:
                sign_up_popup.click()

            # this time.sleep is used for giving time to load data after popup
            time.sleep(5)
            genre_more_btn = driver.find_element(By.CSS_SELECTOR,
                                                    value="html body div#__next div.PageFrame.PageFrame--siteHeaderBanner main.PageFrame__main.BookPage div.BookPage__gridContainer div.BookPage__rightColumn div.BookPage__mainContent div.BookPageMetadataSection div.BookPageMetadataSection__genres ul.CollapsableList div.Button__container").click()

            genre_list = [genre.text for genre in driver.find_elements(
                By.CLASS_NAME, value="BookPageMetadataSection__genreButton")]

            if genre in genre_list:
                book_details_btn = driver.find_element(
                    By.CSS_SELECTOR, value="div.CollapsableList > div:nth-child(3)")
                book_details_btn.click()
                # some books don't have either isbn or language
                try:
                    # if isbn is not present then this line will give language
                    isbn = driver.find_element(
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
                        language = driver.find_element(
                            By.CSS_SELECTOR, "div.DescListItem:nth-child(4) > dd:nth-child(2) > div:nth-child(1) > div:nth-child(1)").text.strip()
                
                if desired_language == language:
                    title = driver.find_element(
                        by=By.TAG_NAME, value="h1").text
                    book_cover_div = driver.find_element(
                        by=By.CLASS_NAME, value="BookCover")
                    book_cover_url = book_cover_div.find_element(
                        By.CLASS_NAME, "ResponsiveImage").get_attribute("src")
                    contributors = driver.find_element(
                        By.CLASS_NAME, value="ContributorLinksList").text.replace("\n ", "").replace("\n", "")
                    description = driver.find_element(
                        By.CLASS_NAME, value="Formatted").get_attribute("innerHTML")
                    page_edition = driver.find_element(
                        By.CSS_SELECTOR, value=".FeaturedDetails > p:nth-child(1)").text
                    
                    num_of_pages = None
                    edition = page_edition
                    if "pages" in page_edition:
                        num_of_pages, edition = page_edition.split(" pages, ")
                        
                    if num_of_pages:
                        num_of_pages = int(num_of_pages)
                        
                    published_date = driver.find_element(By.CSS_SELECTOR, value=".FeaturedDetails > p:nth-child(2)").text.split("published ")[-1]
                    recommended_book_section = driver.find_element(By.CSS_SELECTOR, ".BookPage__relatedTopContent > div:nth-child(1) > div:nth-child(1) > section:nth-child(1) > div:nth-child(2) > div:nth-child(1)")
                    recommended_book_urls = [anchor_tag.get_attribute("href") for anchor_tag in recommended_book_section.find_elements(By.TAG_NAME, "a")]
                    
                    for url in recommended_book_urls:
                        if url not in book_url_list and len(book_url_list) < url_limit:
                            book_url_list.append(url)
                            print(len(book_url_list))
                            
                    
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
                    print(book_item)
                    
                else:
                    print("Did Not Scrape This URL Becuase Language does not match")


    return book_items


def save_data_to_file(book_items):
    """This takes list dictionary which are book_items"""
    df = pandas.DataFrame.from_dict(book_items, orient='columns')
    df.to_csv("books.csv")


book_items = scrape_book_links()
save_data_to_file(book_items=book_items)


