from bs4 import BeautifulSoup
import requests
import csv

#https://www.waitrose.com/api/content-prod/v2/cms/publish/productcontent/browse/-1?clientType=WEB_APP
products=[]

# init the object that holds product details
class product_item:
    def __init__(self, energy="Null", fat_tot="Null", fat_sat="Null", fat_poly="Null", carb="Null", sugar="Null", fibre="Null", protein="Null", salt="Null", omega3="Null", sodium="Null", mvv="meat"):
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


all_products = []

#writing to csv, opening the csv
with open('item_file.csv', mode='w', encoding='utf-8') as item_file:
    item_writer = csv.writer(item_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    #creating the class that will hold data for each entry
    for x in products:
        appended_link = "http://" + x["bsurl"]
        new_class = product_item(x["clubName"], 0, "", appended_link, x.get("listingdescription", "Null"), x["postcode"], "", str("age range:" + x.get("ageFrom", "Null") + "-" + x.get("ageTo", "Null")), "", "", "")
        all_products.append(new_class)

    for item in all_products:
        result = requests.get(f'{item.bus_site}')
        content = result.text
        soup = BeautifulSoup(content, 'lxml')
        try:
            item.bus_phone = (soup.find('i', class_='fa fa-fw fa-phone').parent.get_text())
           
        except: continue  

        try:
             item.bus_email = (str(soup.find('i', class_='fa fa-fw fa-envelope').parent))

        except: continue

        try:
            item.external_site = (str(soup.find('i', class_='fa fa-fw fa-globe').parent))

        except: pass

        #social media info

        try:
            item.facebook = (str(soup.find('i', class_='fab fa-facebook-square').parent))

        except: pass

        try:
            item.twitter = (str(soup.find('i', class_='fab fa-twitter-square').parent))

        except: pass

        try:
            item.instagram = (str(soup.find('i', class_='fab fa-instagram').parent))

        except: pass


        # print(item.bus_name)
        # print(item.bus_phone)
        # print(item.bus_email)
        
        try:
            item_writer.writerow([item.bus_name, item.bus_phone, (item.bus_email), item.bus_site, item.postcode, item.external_site, item.age_range, item.facebook, item.instagram, item.twitter, (item.bus_desc)])
            print("still")
            print("working")
        
        except: 
            print('failed')
            continue  

    
