import random
import time

import requests
from bs4 import BeautifulSoup
from partsfinder.celeryconf import app

from .models import Category, Product

microcenter_url_graphic = "https://www.microcenter.com/search/search_results.aspx?N=4294966937&NTK=all&sortby=match&rpp=48&myStore=false"
microcenter_url_cpu = "https://www.microcenter.com/search/search_results.aspx?N=4294966995&NTK=all&sortby=match&rpp=48&myStore=false"
microcenter_url_memory = "https://www.microcenter.com/search/search_results.aspx?N=4294966653&NTK=all&sortby=match&rpp=48&myStore=false"
microcenter_url_mainBroad = "https://www.microcenter.com/search/search_results.aspx?N=4294966996&NTK=all&sortby=match&rpp=48&myStore=false"
microcenter_url_power = "https://www.microcenter.com/search/search_results.aspx?Ntk=all&sortby=match&N=4294966654&rpp=48&myStore=false"
microcenter_url_pcCase = "https://www.microcenter.com/search/search_results.aspx?N=4294964318&NTK=all&sortby=match&rpp=48&myStore=false"
microcenter_url_ssd = "https://www.microcenter.com/search/search_results.aspx?N=4294966958&NTK=all&sortby=match&rpp=48&myStore=false"
centralcomputer_url_graphic = "https://www.centralcomputer.com/all-products/hardware/video-cards.html"
centralcomputer_url_cpu = "https://www.centralcomputer.com/all-products/hardware/cpus.html"
centralcomputer_url_memory = "https://www.centralcomputer.com/all-products/hardware/memory.html"
centralcomputer_url_mainBroad = "https://www.centralcomputer.com/all-products/hardware/motherboards.html"
centralcomputer_url_power = "https://www.centralcomputer.com/all-products/hardware/power-supplies.html"
centralcomputer_url_pcCase = "https://www.centralcomputer.com/all-products/hardware/cases-chassis.html"
centralcomputer_url_ssd = "https://www.centralcomputer.com/all-products/hardware/hard-drives-ssd.html"

lst_microcenter = [microcenter_url_cpu, microcenter_url_graphic, microcenter_url_mainBroad,
                   microcenter_url_pcCase, microcenter_url_memory, microcenter_url_power, microcenter_url_ssd]
lst_centralcomputer = [centralcomputer_url_cpu, centralcomputer_url_graphic, centralcomputer_url_mainBroad,
                       centralcomputer_url_pcCase, centralcomputer_url_memory, centralcomputer_url_power, centralcomputer_url_ssd]


@app.task
def crawl_data():
    category_lst = Category.objects.all().order_by("id")
    product_lst = []
    product_lst_print = []
    for category, url in zip(category_lst, lst_microcenter):
        req = requests.get(url, 'html.parser')
        soup = BeautifulSoup(req.content, 'html.parser')
        list_products = soup.findAll("li", {"class": "product_wrapper"})
        for i in list_products:
            li_div = i.find("div", {"class": "result_right"})
            name = li_div.find("a").text
            product_id = li_div.find("a").attrs["data-id"]
            div_price = li_div.find("div", {"class": "price"}).find_all("span")
            try:
                li_div_avalible = li_div.find(
                    "span", {"class": "availabilityTrunc"}).text
            except:
                li_div_avalible = li_div.find("div", {"class": "stock"}).text
            div_left = i.find("div", {"class": "result_left"})
            img = div_left.find(
                "img", {"class": "SearchResultProductImage"}).attrs["src"]
            url = li_div.find("div", {"class": "normal"}).find(
                "a").attrs["href"]
            available = True if 'Available' in li_div_avalible else False
            urls = "https://www.microcenter.com" + str(url.strip())
            for k in div_price:
                if k.text != '$':
                    price = k.text
            obj = {
                'productId': int(product_id),
                'name': name,
                'price': float(price[1::].strip().replace(',', '')),
                'urls': urls,
                'thumbnail': img,
                'available': available,
                'category_id': category.id,
                'source': "microcenter"
            }
            product_lst_print.append(obj)
            product_model = Product(**obj)
            product_lst.append(product_model)
    for category, url in zip(category_lst, lst_centralcomputer):
        req = requests.get(url, 'html.parser')
        soup_central = BeautifulSoup(req.content, 'lxml')
        lst_product_central = soup_central.find_all(
            "li", {"class": "item product product-item"})
        for i in lst_product_central:
            href = i.find("a", {"class": "product-item-link"}).attrs["href"]
            name = i.find("a", {"class": "product-item-link"}).text
            img = i.find("img", {"class": "product-image-photo"}).attrs["src"]
            try:
                productId = i.find(
                    "div", {"class": "price-box price-final_price"}).attrs["data-product-id"]
            except:
                productId = random.randint(1, 1000000)
            try:
                avalible = i.find(
                    "div", {"class": "inStokHolder"}).find("label").text
            except:
                try:
                    avalible = i.find(
                        "div", {"class": "special-order-holder"}).find("label").text
                except:
                    avalible = ""
            price_dev = i.find("div", {"class": "product-item-inner"})
            try:
                price = price_dev.find("span", {
                                       "class": "price-container price-final_price tax weee"}).find("span", {"class": "price"}).text
            except:
                price = "00"
            urls = href.strip()
            available = False if 'Order' in avalible else True
            obj = {
                'productId': int(productId),
                'name': name.strip(),
                'price': float(price[1::].strip().replace(',', '')),
                'urls': urls.strip(),
                'thumbnail': img.strip(),
                'available': available,
                'category_id': category.id,
                'source': "centralcomputer"
            }
            product_lst_print.append(obj)
            product_model = Product(**obj)
            product_lst.append(product_model)
    # with open('core/products/test.txt','w') as f:
    #     f.write(str(product_lst_print))
    Product.objects.all().delete()
    Product.objects.bulk_create(product_lst)
