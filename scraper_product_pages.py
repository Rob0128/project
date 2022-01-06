from os import name
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import mysql.connector


class item:

    def __init__(self, title="", category_broad="", category_specific="", item_link="", energy="", fat_tot="", fat_sat="", fat_poly="", carb="", sugar="", fibre="", protein="", salt="", omega3="", sodium="", mvv="meat"):
        
        self.title = title
        self.category_broad = category_broad
        self.category_specific = category_specific
        self.item_link = item_link
        self.energy = energy
        self.fat_total = fat_tot
        self.fat_saturated = fat_sat
        self.fat_poly = fat_poly
        self.carb = carb
        self.sugar = sugar
        self.fibre = fibre
        self.protein = protein
        self.salt = salt
        self.omega3 = omega3
        self.sodium = sodium
        self.meat_or_veg = mvv
        

class page_scraper:

    def __init__(self) -> None:
        super().__init__()

    def query_builder():

        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Supergreen28!",
        database="proj_schema"
        )

        mycursor = mydb.cursor()

        sql = "SELECT link FROM product_links"
        mycursor.execute(sql)

        prod_links = mycursor.fetchall()

        print("Total number of rows in table: ", mycursor.rowcount)

        return prod_links


    def scrape_pages(self, prod_links):

        for link in prod_links:
            self.process_page(link)


    def process_page(link):
        
        #scrape each page here

        current_item = item

        s = HTMLSession()
        url = link

        r = s.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        #populate the item object with data from the page
        
        current_item.title = (soup.find('h1', class_='title___31Yu2').get_text())
        
        #returns all text from the breadcrumb bar
        category_uncleaned = (soup.find('ul', class_='crumbs___3NtHD').get_text(","))
        #split the texts with a comma and split them into a list to make them accessable individually
        category_list = category_uncleaned.split(",")
        current_item.category_broad  = category_list[2]
        current_item.category_specific = category_list[3]

        print(current_item.category_broad, current_item.category_specific)
        #access engery on page and then add the value to the line below
        #current_item.energy =  

        return "object (current_item) with product info"


    def load_to_db(self, arr):
        
        print("ltd")
        for link in arr:
            self.query_builder(self, link)



if __name__ == "__main__":

    links = page_scraper.query_builder()
    page_scraper.process_page('https://www.waitrose.com/ecom/products/activia-fat-free-cherry-yogurts/783167-690830-690831')
