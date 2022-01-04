from selenium import webdriver      
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class webscraper(object):


    def __init__(self) -> None:
        super().__init__()

    def open_browser(self):
        WAITROSE_SEARCH_PAGE_URL = "https://www.waitrose.com/ecom/shop/browse/groceries"
        PATIENCE_TIME = 50
        LOAD_MORE_BUTTON_XPATH = '//*[@id="browse-itemsprimary"]/li[2]/button/span/span[2]' 

        driver = webdriver.Chrome('C:\chromedriver\chromedriver.exe')

        driver.get(WAITROSE_SEARCH_PAGE_URL)

        #deal with cookie popup
        driver.implicitly_wait(10)

        driver.find_element_by_xpath('//*[@data-webviewid="accept-cookies"]').click()

        return driver
    
    def load_pages(self, driver):
        count = 0

        while True:
            try:
                loadMoreButton = driver.find_element_by_xpath("//button[contains(@aria-label,'Load more')]")
                time.sleep(3)
                loadMoreButton.click()
                count += 1
                time.sleep(4)
                print(count)
                if count >= 4:
                    break
                
            except Exception as e:
                print(e)
                break

    # elements = driver.find_elements_by_xpath("//header[@class='podHeader___2KpI7']/a")
    # arr = []
    # new_str=""
    # for element in elements:
    #     href = element.get_attribute("href")
    #     arr.append(href)

    #     print(arr)


            #elements = driver.find_elements_by_class_name("podHeader___2KpI7") 

        print("done")
        print(count)
        driver.quit()

if __name__ == "__main__":
    scrpr = webscraper
    driver = webscraper.open_browser(scrpr)
    webscraper.load_pages(scrpr, driver)
    



# search_box.send_keys('ChromeDriver')

# search_box.submit()


