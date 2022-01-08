from os import name
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import mysql.connector
import re


class item:

    def __init__(self, title="", category_broad="", category_specific="", item_link="", serving_description="", energy_kj=0, energy_cal=0, fat_tot=0, fat_sat=0, fat_poly=0, carb=0, sugar=0, fibre=0, protein=0, salt=0, omega3=0, sodium=0, mvv="meat"):
        
        self.title = title
        self.category_broad = category_broad
        self.category_specific = category_specific
        self.item_link = item_link
        self.serving_description = serving_description
        self.energy_kj = energy_kj
        self.energy_cal = energy_cal
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

    #connect to db and load list of product web addresses
    def get_links_from_db():

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


    def process_page(link):
        
        #scrape each page here

        current_item = item

        s = HTMLSession()
        url = link

        r = s.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        #populate the item object with data from the page

        if soup.find('div', class_='nutrition___30wTj'):
            
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


            # check if collumn for per serve values
            whole_table = (soup.find('div', class_='nutrition___30wTj'))
            column_headers = (whole_table.find_all('thead'))
            count_check = str(column_headers).count("<td>")
            print(column_headers)

            if count_check == 2:

            #record description of a serving size
                split_headers = column_headers[0].find_all('td')[1].text

                
            # all_th = soup.find_all('tr')
            
            #print(all_th[5].get_text())

            
                #find individual values
                table_values = str(whole_table.find_all('tbody'))
                reduced_values = table_values.split("<tr>")

            

                for x in range(1, len(reduced_values) - 1):
                    
                    ex = (reduced_values[x].split(">"))
                    
                    #table_values_clean = []
                    title = ex[1].split("<")[0]

                    #use this to access 100g value
                    #first_val = (ex[3].split("<")[0].replace("g", ""))

                    second_val = ex[5].split("<")[0].replace("g", "").replace(" ", "").replace("&lt;", "")
                    print(title, second_val)

                    #add to appropriate object variable
                    energy_second = False

                    if title == "Energy" and energy_second == False:
                        print("got it", int(re.sub("[^0-9]", "", second_val)))
                        current_item.energy_kj = int(re.sub("[^0-9]", "", second_val))
                        energy_count = True

                    if title == "Energy" and energy_second == True:
                        print("got it", int(re.sub("[^0-9]", "", second_val)))
                        current_item.energy_cal= int(re.sub("[^0-9]", "", second_val))

                    if title == "Fat":
                        print("got it", second_val)
                        current_item.fat_total = float(second_val)
                    
                    if title == "Of which Saturates":
                        print("got it", second_val)
                        current_item.fat_saturated = float(second_val)

                    if title == "Carbohydrate":
                        print("got it", second_val)
                        current_item.carb = float(second_val)

                    if title == "Of which Sugars":
                        print("got it", second_val)
                        current_item.sugar = float(second_val)

                    if title == "Fibre":
                        print("got it", second_val)
                        current_item.fibre = float(second_val)

                    if title == "Protein":
                        print("got it", second_val)
                        current_item.protein = float(second_val)

                    if title == "Salt":
                        print("got it", second_val)


        return current_item

    def scrape_pages(self, prod_links):

        for link in prod_links:
            print(link[0])
            prod_item = self.process_page(link[0])
            self.upload_to_db(prod_item)


    def upload_to_db(item_object):

        
        return "done" 

    def query_update(up_item, up_val):
        return "hi" 

    # def load_to_db(self, arr):
        
    #     print("ltd")
    #     for link in arr:
    #         self.process_page(link)

    #         #self.query_builder(self, link)



if __name__ == "__main__":

    links = page_scraper.get_links_from_db()
    scraper_instance = page_scraper
    page_scraper.scrape_pages(scraper_instance, links)


    #page_scraper.process_page('https://www.waitrose.com/ecom/products/essential-greek-style-natural-yogurt/565210-80062-80063')
