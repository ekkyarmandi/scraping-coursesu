import requests
from bs4 import BeautifulSoup
import re

headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}

def scraper(src_url,html):
    
    # turn html into bs4 object
    page = BeautifulSoup(html,"html.parser")

    # find product name
    try: product_name = page.find("h1",{"class":"product-name"}).get_text().strip()
    except: product_name = None

    # find product categories
    try:
        categories = page.find("div",{"class":"breadcrumb clearfix pdp-breadcrumb"}).find_all("a")
        categories = [c.get_text().strip() for c in categories]
        categories = [c for c in categories if len(c) > 0]
        categories = "; ".join(categories) + ";"
    except:
        categories = None

    # find product image url
    try:
        context = {"itemprop": "image","class": "primary-image"}
        image_url = page.find("img",context)['src']
    except:
        image_url = None

    # find product brand
    product_brand = None
    for tag in page.find_all():
        if "brand" in str(tag) and tag.has_attr("alt"):
            product_brand = tag['alt']
            break

    # find product nutriscore
    nutriscore = None
    for tag in page.find_all():
        if "nutriscore" in str(tag) and tag.has_attr("alt"):
            nutriscore = tag['alt']
            break

    # find product ingredients and calories
    product_informations = {}
    informations = page.find("div",{"class":"main-information-content"})
    for info in informations.find_all("h3"):
        title = info.get_text().strip().lower().replace(" ","_")
        text = info.find_next("p").get_text().strip()
        product_informations.update({title:text})
        
    try:
        ingredients = product_informations['ingrédients']
        ingredients = re.sub("\s+"," ",ingredients).strip()
    except: ingredients = None

    calories = None
    try:
        nutritions = product_informations['valeurs_nutritionnelles']
        nutritions = [n.strip() for n in nutritions.split(",") if "kcal" in n]
        if len(nutritions) > 0:
            calories = ", ".join(nutritions)
    except: pass

    # find product calories from table
    try:
        context = {
            "class": "tab-content",
            "data-tabcontent": "tab-nutritional",
            "role": "tabpanel"
        }
        table = page.find("div",context)
        header = table.find("header").get_text().strip()
        for row in table.find("section").find_all("div",{"class":"info-row"}):
            value = row.find("div",{"class":"value"}).get_text()
            value = re.sub("\s+"," ",value).strip()
            value = re.search("\d+ kcal",value).group()
            break
        
        calories = f"{header} = {value}"
    except:
        calories = None

    # find product origin through further more information
    further_informations = {}
    context = {
        "class": "toggle-information-content",
        "data-togglecontent": "Further Information"
    }
    informations = page.find("div",context)
    for info in informations.find_all("h3"):
        title = info.get_text().strip().lower().replace(" ","_")
        text = info.find_next("div").get_text().strip()
        further_informations.update({title:text})
        
    try:
        origin_info = further_informations['informations_complémentaires']
        origin_info = re.sub("\s+"," ",origin_info).strip()
    except: origin_info = None

    product_data = {
        "url": src_url,
        "image_url": image_url,
        "name": product_name,
        "brand": product_brand,
        "nutriscore": nutriscore,
        "categories": categories,
        "ingredients": ingredients,
        "calories": calories,
        "manufactured_at": origin_info,
        "code": None
    }
    return product_data

if __name__ == '__main__':

    url = "https://www.coursesu.com/p/cerneau-de-noix-sachet-de-500g/1043005.html"
    req = requests.get(url, headers=headers)
    data = scraper(url,req.text)
    print(data)