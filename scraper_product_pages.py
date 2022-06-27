from os import name
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import mysql.connector
import re


class item:

    def __init__(self, title="", category_broad="", category_specific="", item_link="", serving_description="", energy_kj=0, energy_cal=0, fat_tot=0, fat_sat=0, carb=0, sugar=0, fibre=0, protein=0, salt=0, mvv="meat"):
        
        self.title = title
        self.category_broad = category_broad
        self.category_specific = category_specific
        self.item_link = item_link
        self.serving_description = serving_description
        self.energy_kj = energy_kj
        self.energy_cal = energy_cal
        self.fat_total = fat_tot
        self.fat_saturated = fat_sat
        self.carb = carb
        self.sugar = sugar
        self.fibre = fibre
        self.protein = protein
        self.salt = salt
        self.meat_or_veg = mvv
        

class page_scraper:

    def __init__(self) -> None:
        super().__init__()

    #connect to db and load list of product web addresses
    def get_links_from_db():

        mydb = mysql.connector.connect(
        host="DESKTOP-NOE172B", #DESKTOP-NOE172B
        user="M3H\rob.hill", #M3H\rob.hill
        passwd="",
        database="Projects"
        )

        mycursor = mydb.cursor()

        sql = "SELECT link FROM product_links"
        mycursor.execute(sql)

        prod_links = mycursor.fetchall()

        print("Total number of rows in table: ", mycursor.rowcount)

        return prod_links


    def process_page(link):
        
        #scrape each page here

        

        s = HTMLSession()
        url = link

        r = s.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        #populate the item object with data from the page


        current_item = item

        #variable to check if checks passed and object should be returned
        ret_object = False


        if soup.find('div', class_='nutrition___30wTj'):

            
            
            


            # check if collumn for per serve values
            whole_table = (soup.find('div', class_='nutrition___30wTj'))
            column_headers = (whole_table.find_all('thead'))
            count_check = str(column_headers).count("<td>")
            print(column_headers)


            

            if count_check == 2:

                ret_object= True

                current_item.title = (soup.find('h1', class_='title___31Yu2').get_text())

                current_item.item_link = link

                #returns all text from the breadcrumb bar
                category_uncleaned = (soup.find('ul', class_='crumbs___3NtHD').get_text(","))
                #split the texts with a comma and split them into a list to make them accessable individually
                category_list = category_uncleaned.split(",")
                print(category_list)
                current_item.category_broad  = category_list[2]
                current_item.category_specific = category_list[3]

                print("hi")
                print(current_item.category_broad, current_item.category_specific)
           
                #record description of a serving size
                #desc_headings = column_headers.find_all('td')
                
                
                current_item.serving_description = column_headers[0].find_all('td')[1].text
                current_item.meat_or_veg = "none"
                
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
                        energy_second = True

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
                        current_item.salt = float(second_val)

            
        if ret_object == True:    
            return current_item
        else:
            return 0
        
        

    def scrape_pages(self, prod_links):

        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Supergreen28!",
        database="proj_schema")

        mycursor = mydb.cursor()

        for link in prod_links:
            
            cur_item = self.process_page(link[0])

            if type(cur_item) != int:
                self.upload_to_db(cur_item, mydb, mycursor)


    def upload_to_db(cur_object, db, cursor):

        print("SSSSTTTAARRTTIINNGG")
        # for attr, value in cur_object.__dict__.items():
        #     if not attr.startswith('__'):
        #         print(attr)

        print(cur_object.category_broad)
        sql = "INSERT INTO product_info (title, category_broad, category_specific, item_link, serving_description, energy_kj, energy_cal, fat_total, fat_saturated, carb, sugar, fibre, protein, salt, meat_or_veg) VALUES (" + "\"" + str(cur_object.title) + "\"" + ", " + "\"" + str(cur_object.category_broad) + "\"" + ", " + "\"" + str(cur_object.category_specific) + "\"" + ", " + "\"" + str(cur_object.item_link) + "\"" + ", " + "\"" + str(cur_object.serving_description) + "\"" + ", " + "\"" + str(cur_object.energy_kj)  + "\"" + ", " + "\"" + str(cur_object.energy_cal) + "\"" + ", " + "\"" + str(cur_object.fat_total) + "\"" + ", " + "\"" + str(cur_object.fat_saturated) + "\"" + ", " + "\"" + str(cur_object.carb)  + "\"" + ", " + "\"" + str(cur_object.sugar)  + "\"" + ", " + "\"" + str(cur_object.fibre) + "\"" + ", " + "\"" + str(cur_object.protein)  + "\"" + ", " + "\"" + str(cur_object.salt) + "\"" + ", " + "\"" + str(cur_object.meat_or_veg) + "\"" + ")"
        
        print(sql)
        
        cursor.execute(sql,)

        db.commit()

        print("it worked") 



if __name__ == "__main__":

    links = page_scraper.get_links_from_db()
    scraper_instance = page_scraper
    page_scraper.scrape_pages(scraper_instance, links)


    #page_scraper.process_page('https://www.waitrose.com/ecom/products/essential-greek-style-natural-yogurt/565210-80062-80063')



