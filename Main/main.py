import time
import smtplib
import requests
from bs4 import BeautifulSoup


def log(file_name, data_to_log):
    with open(file_name, "a") as file:
        file.write("\n")
        file.write(str(str(time.strftime('[%a %d-%m-%Y %H:%M:%S]', time.gmtime())).upper()) + ":" + str(data_to_log))


def read_file(file_name):
    with open(file_name, "r") as file:
        return file.read()


def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False


def send_gmail(email_from, password_from, email_to, email_subject, email_body):
    gmail_server = smtplib.SMTP('smtp.gmail.com', 587)
    gmail_server.ehlo()
    gmail_server.starttls()
    gmail_server.login(email_from, password_from)
    email_content = str(
        f"From: {str(email_from)}\nTo: {str(email_to)}\nSubject: {str(email_subject)}\n\n{str(email_body)}")
    gmail_server.sendmail(email_from, email_to, email_content)


# PCCG Test URLS
# pre "https://www.pccasegear.com/products/51041/phanteks-enthoo-pro-2-closed-panel-full-tower-case-black"
# sold out "https://www.pccasegear.com/products/51766/gigabyte-geforce-rtx-3080-vision-oc-10gb"
# in stock "https://www.pccasegear.com/products/51821/8ware-hdmi-1-4-cable-1-8m"

pccg_test_urls = ["https://www.pccasegear.com/products/51821/8ware-hdmi-1-4-cable-1-8m",
                  "https://www.pccasegear.com/products/51041/phanteks-enthoo-pro-2-closed-panel-full-tower-case-black",
                  "https://www.pccasegear.com/products/51766/gigabyte-geforce-rtx-3080-vision-oc-10gb"]


def pccg(url):
    page = requests.get(url)
    parse = BeautifulSoup(page.content, 'html.parser')
    # print(parse)
    try:
        stock_level = parse.find("button", class_="add-to-cart").text.split('\n\n')[0].strip()
        # print(stock_level)
        if stock_level == "Add to Cart":
            return 2
        elif stock_level == "Pre-Order":
            return 1
        elif stock_level == "Sold Out":
            return 0
        else:
            return 404
    except AttributeError:
        return 404


# for i in pccg_test_urls:
# print(pccg(i))

# Expected output 2 1 0

# Scorptec Test URLS
# pre "https://www.scorptec.com.au/product/headphones/accessories/82212-mpa-gs750-00-i1"
# eta "https://www.scorptec.com.au/product/monitors/25plus-inch/84342-34wn750-b"
# at supplier "https://www.scorptec.com.au/product/cases/atx/74070-ca-3k7-50m1na-00"
# sold out "https://www.scorptec.com.au/product/graphics-cards/nvidia/85382-rog-strix-rtx3080-o10g-gaming"
# in stock "https://www.scorptec.com.au/product/branded-systems/gaming-systems/85679-meg-infinite-x-10te-850au"
# 1 "https://www.scorptec.com.au/product/laptops-&-notebooks/laptops/81236-7qz78pa"

scorptec_test_urls = [
    "https://www.scorptec.com.au/product/branded-systems/gaming-systems/85679-meg-infinite-x-10te-850au",
    "https://www.scorptec.com.au/product/laptops-&-notebooks/laptops/81236-7qz78pa",
    "https://www.scorptec.com.au/product/cases/atx/74070-ca-3k7-50m1na-00",
    "https://www.scorptec.com.au/product/monitors/25plus-inch/84342-34wn750-b",
    "https://www.scorptec.com.au/product/headphones/accessories/82212-mpa-gs750-00-i1",
    "https://www.scorptec.com.au/product/graphics-cards/nvidia/85382-rog-strix-rtx3080-o10g-gaming"]


def scorptec(url):
    page = requests.get(url)
    parse = BeautifulSoup(page.content, 'html.parser')
    # print(parse)
    try:
        stock_level = parse.find("div", class_="product-stock-text").text.split("\n\n")[1]
        # print(stock_level)
        if stock_level == "In Stock" or stock_level == "At Supplier" or stock_level == "Limited Stock" or is_int(
                stock_level[0]):
            return 2
        elif stock_level == "PRE-ORDER" or stock_level[:3] == "ETA":
            return 1
        elif stock_level == "SOLD OUT":
            return 0
        else:
            return 404
    except AttributeError:
        return 404


# for i in scorptec_test_urls:
# print(scorptec(i))

# Expected output 2 2 2 1 1 0

# Mwave Test Urls
# in stock "https://www.mwave.com.au/product/warzone-geforce-esports-pro-gaming-pc-rtx-3060-ti-edition-ac40581"
# at supplier "https://www.mwave.com.au/product/ekwb-ekquantum-vector-drgb-xc3-rtx-30803090-gpu-water-
#                                                                                           block-nickel-acetal-ac40364"
# sold out "https://www.mwave.com.au/product/asus-geforce-rtx-3080-rog-strix-oc-10gb-video-card-ac38206"
# pre "https://www.mwave.com.au/product/gigabyte-aorus-geforce-rtx-3080-waterforce-10gb-gaming-box-ac40415"


# def mwave(url):
# page = requests.get(url)
# parse = BeautifulSoup(page.content, 'html.parser')
# print(parse)
# stock_level = parse.find("div", class_="basicInfos").text.split("\n\n")[0].strip()
# print(stock_level)


# mwave("https://www.mwave.com.au/product/warzone-geforce-esports-pro-gaming-pc-rtx-3060-ti-edition-ac40581")

# Centrecom Test URLS
# in stock "https://www.centrecom.com.au/cooler-master-masterbox-td500-argb-mesh-case"
# pre "https://www.centrecom.com.au/thermaltake-suppressor-f1-mini-itx-case"
# sold out "https://www.centrecom.com.au/msi-geforce-rtx-3080-gaming-x-trio-10g-graphics-card#popup_stock"
# in store "https://www.centrecom.com.au/silverstone-sugo-series-sg13-mini-itx-case-blackwhitemesh-front-panel"

centrecom_test_urls = ["https://www.centrecom.com.au/cooler-master-masterbox-td500-argb-mesh-case",
                       "https://www.centrecom.com.au/thermaltake-suppressor-f1-mini-itx-case",
                       "https://www.centrecom.com.au/silverstone-sugo-series-sg13-mini-itx-case-blackwhitemesh-front"
                       "-panel",
                       "https://www.centrecom.com.au/msi-geforce-rtx-3080-gaming-x-trio-10g-graphics-card#popup_stock"]


def centrecom(url):
    page = requests.get(url)
    parse = BeautifulSoup(page.content, 'html.parser')
    # print(parse)
    try:
        stock_level = parse.find("button", class_="prod_addtocart").text.split("\n\n")[0].strip()
        # print(stock_level)
        if stock_level == "Add to cart":
            return 2
        elif stock_level[:9] == "Pre-Order":
            return 1
    except AttributeError:
        try:
            stock_level = parse.find("div", class_="prod_instorebutton").text.split("\n\n")[0].strip()
            # print(stock_level)
            if stock_level == "Sold Out":
                return 0
            elif stock_level == "In-store only":
                return 3
        except AttributeError:
            return 404


# for i in centrecom_test_urls:
# print(centrecom(i))

# Expected output 2 1 3 0


def main():
    with open("log.txt", "a+") as file:
        file.write("\n\nNEW SESSION")
    pccg_urls = read_file("pccg_urls.txt").split("\n")
    scorptec_urls = read_file("scorptec_urls.txt").split("\n")
    centrecom_urls = read_file("centrecom_urls.txt").split("\n")
    gmail_settings = read_file("gmail_settings.txt").split("\n")
    gmail_username = gmail_settings[0][15:]
    gmail_app_password = gmail_settings[1][19:]
    gmail_to = gmail_settings[2][3:]
    pccg_stock = {}
    scorptec_stock = {}
    centrecom_stock = {}
    while True:
        if pccg_urls[0] != "":
            for i in pccg_urls:
                if pccg_stock.get(i) is None:
                    pccg_stock[i] = 0
                pccg_result = pccg(i)
                if pccg_result == 2 and pccg_stock.get(i) != 2:
                    pccg_stock[i] = 2
                    send_gmail(gmail_username, gmail_app_password, gmail_to,
                               "Python Stock Alert", f"PCCG Item {i} has Stock Available")
                if pccg_result == 1 and pccg_stock.get(i) != 1:
                    pccg_stock[i] = 1
                    send_gmail(gmail_username, gmail_app_password, gmail_to,
                               "Python Stock Alert", f"PCCG Item {i} is Available for Pre-Order")
                if pccg_result == 404 and pccg_stock.get(i) != 404:
                    pccg_stock[i] = 404
                    send_gmail(gmail_username, gmail_app_password, gmail_to,
                               "Python Stock Alert ERROR", f"ERROR url: {i} is invalid")
                pccg_stock[i] = pccg_result
        if scorptec_urls[0] != "":
            for i in scorptec_urls:
                if scorptec_stock.get(i) is None:
                    scorptec_stock[i] = 0
                scorptec_result = scorptec(i)
                if scorptec_result == 2 and scorptec_stock.get(i) != 2:
                    scorptec_stock[i] = 2
                    send_gmail(gmail_username, gmail_app_password, gmail_to,
                               "Python Stock Alert", f"Scorptec Item {i} has Stock Available")
                if scorptec_result == 1 and scorptec_stock.get(i) != 2:
                    scorptec_stock[i] = 1
                    send_gmail(gmail_username, gmail_app_password, gmail_to,
                               "Python Stock Alert", f"Scorptec Item {i} is Available for Pre-Order")
                if scorptec_result == 404 and scorptec_stock.get(i) != 404:
                    scorptec_stock[i] = 404
                    send_gmail(gmail_username, gmail_app_password, gmail_to,
                               "Python Stock Alert", f"ERROR url: {i} is invalid")
                scorptec_stock[i] = scorptec_result
        if centrecom_urls[0] != "":
            for i in centrecom_urls:
                if centrecom_stock.get(i) is None:
                    centrecom_stock[i] = 0
                centrecom_result = centrecom(i)
                if centrecom_result == 2 and centrecom_stock.get(i) != 2:
                    centrecom_stock[i] = 2
                    send_gmail(gmail_username, gmail_app_password, gmail_to, "Python Stock Alert",
                               f" Centrecom Item {i} has Stock Available")
                if centrecom_result == 1 and centrecom_stock.get(i) != 1:
                    centrecom_stock[i] = 1
                    send_gmail(gmail_username, gmail_app_password, gmail_to, "Python Stock Alert",
                               f"Centrecom Item {i} is Available for Pre-Order")
                if centrecom_result == 404 and centrecom_stock.get(i) != 404:
                    centrecom_stock[i] = 404
                    send_gmail(gmail_username, gmail_app_password, gmail_to, "Python Stock Alert",
                               f" ERROR url: {i} is invalid")
                if centrecom_result == 3 and centrecom_stock.get(i) != 3:
                    centrecom_stock[i] = 3
                    send_gmail(gmail_username, gmail_app_password, gmail_to, "Python Stock Alert",
                               f"Centrecom Item {i} is Available In Store")
                centrecom_stock[i] = centrecom_result
        time.sleep(30)


if __name__ == '__main__':
    main()
