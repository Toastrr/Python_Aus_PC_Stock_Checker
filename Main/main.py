import time
import smtplib
import requests
import json
from bs4 import BeautifulSoup

logging = 0


def log(file_name, data_to_log):
    if logging != 0:
        with open(file_name, "a+") as file:
            file.write("\n")
            file.write(
                str(str(time.strftime('[%a %d-%m-%Y %H:%M:%S]', time.gmtime())).upper()) + ":" + str(data_to_log))


def read_file(file_name):
    with open(file_name, "r") as file:
        return file.read()


def write_json(file_name, dictionary):
    with open(file_name, "w+") as file:
        file.write(json.dumps(dictionary))


def read_json(file_name):
    try:
        with open(file_name, "r+") as file:
            return json.loads(file.read())
    except FileNotFoundError:
        write_json(file_name, {})
        return {}


def create_file_if_it_doesnt_exist(filename, content=None):
    try:
        with open(filename, "r") as file:
            file.read()
    except FileNotFoundError:
        with open(filename, "w+") as file:
            if not content:
                file.write("")
            else:
                file.write(content)


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


def pcpartpicker(url):
    page = requests.get(url)
    parse = BeautifulSoup(page.content, 'html.parser')
    try:
        stock_levels = [i.strip() for i in parse.find("table", class_="xs-col-12").text.split("\n\n") if i][1:]
        in_stock = 0
        preorder = 0
        out_of_stock = 0
        for i in stock_levels:
            if i == "In stock":
                in_stock += 1
            elif i == "Preorder":
                preorder += 1
            elif i == "Out of stock":
                out_of_stock += 1
            else:
                continue
        if in_stock > 0:
            return in_stock + 2
        elif preorder > 0:
            return 1
        else:
            return 0
    except AttributeError:
        return 404


def main():
    log("log.txt", "\n\nNEW SESSION")
    create_file_if_it_doesnt_exist("gmail_settings.txt", content="gmail_username=\ngmail_app_password=\nto=")
    create_file_if_it_doesnt_exist("pccg_urls.txt")
    create_file_if_it_doesnt_exist("scorptec_urls.txt")
    create_file_if_it_doesnt_exist("centrecom_urls.txt")
    create_file_if_it_doesnt_exist("pcpartpicker_urls.txt")
    gmail_settings = read_file("gmail_settings.txt").split("\n")
    log("log.txt", "Reading Url Files")
    pccg_urls = read_file("pccg_urls.txt").split("\n")
    scorptec_urls = read_file("scorptec_urls.txt").split("\n")
    centrecom_urls = read_file("centrecom_urls.txt").split("\n")
    pcpartpicker_urls = read_file("pcpartpicker_urls.txt").split("\n")
    log("log.txt", "Url Files Read")
    log("log.txt", "Getting Gmail Settings")
    gmail_username = gmail_settings[0][15:]
    gmail_app_password = gmail_settings[1][19:]
    gmail_to = gmail_settings[2][3:]
    log("log.txt", "Gmail Settings Created")
    pccg_stock = read_json("pccg_stock_json.txt")
    scorptec_stock = read_json("scorptec_stock_json.txt")
    centrecom_stock = read_json("centrecom_stock_json.txt")
    pcpartpicker_stock = read_json("pcpartpicker_stock_json.txt")
    log("log.txt", "Starting Loop")
    loop_count = 0
    while True:
        log("log.txt", f"Loop Start, Loop Number: {loop_count}")

        if pccg_urls[0] != "":
            log("log.txt", "pccg_urls.txt not empty beginning scraping")
            for i in pccg_urls:
                if pccg_stock.get(i) is None:
                    log("log.txt", f"{i} not in dict adding to dict")
                    pccg_stock[i] = 0
                log("log.txt", f"current value in dict is {pccg_stock.get(i)}")
                log("log.txt", f"getting {i} data")
                pccg_result = pccg(i)
                log("log.txt", f"data received response is {pccg_result}")
                if pccg_result == 2 and pccg_stock.get(i) != 2:
                    pccg_stock[i] = 2
                    log("log.txt", "value in dict changed to 2")
                    log("log.txt", "sending gmail")
                    send_gmail(gmail_username, gmail_app_password, gmail_to,
                               "Python Stock Alert", f"PCCG Item {i} has Stock Available")
                    log("log.txt", "gmail sent")
                if pccg_result == 1 and pccg_stock.get(i) != 1:
                    pccg_stock[i] = 1
                    log("log.txt", "value in dict changed to 1")
                    log("log.txt", "sending gmail")
                    send_gmail(gmail_username, gmail_app_password, gmail_to,
                               "Python Stock Alert", f"PCCG Item {i} is Available for Pre-Order")
                    log("log.txt", "gmail sent")
                if pccg_result == 404 and pccg_stock.get(i) != 404:
                    pccg_stock[i] = 404
                    log("log.txt", "value in dict changed to 404")
                    log("log.txt", "sending gmail")
                    send_gmail(gmail_username, gmail_app_password, gmail_to,
                               "Python Stock Alert ERROR", f"ERROR url: {i} is invalid")
                    log("log.txt", "gmail sent")
                pccg_stock[i] = pccg_result
                write_json("pccg_stock_json.txt", pccg_stock)

        if scorptec_urls[0] != "":
            log("log.txt", "scorptec_urls.txt not empty beginning scraping")
            for i in scorptec_urls:
                if scorptec_stock.get(i) is None:
                    scorptec_stock[i] = 0
                    log("log.txt", f"{i} not in dict adding to dict")
                log("log.txt", f"current value in dict is {scorptec_stock.get(i)}")
                log("log.txt", f"getting {i} data")
                scorptec_result = scorptec(i)
                log("log.txt", f"data received response is {scorptec_result}")
                if scorptec_result == 2 and scorptec_stock.get(i) != 2:
                    scorptec_stock[i] = 2
                    log("log.txt", "value in dict changed to 2")
                    log("log.txt", "sending gmail")
                    send_gmail(gmail_username, gmail_app_password, gmail_to,
                               "Python Stock Alert", f"Scorptec Item {i} has Stock Available")
                    log("log.txt", "gmail sent")
                if scorptec_result == 1 and scorptec_stock.get(i) != 1:
                    scorptec_stock[i] = 1
                    log("log.txt", "value in dict changed to 1")
                    log("log.txt", "sending gmail")
                    send_gmail(gmail_username, gmail_app_password, gmail_to,
                               "Python Stock Alert", f"Scorptec Item {i} is Available for Pre-Order")
                    log("log.txt", "gmail sent")
                if scorptec_result == 404 and scorptec_stock.get(i) != 404:
                    scorptec_stock[i] = 404
                    log("log.txt", "value in dict changed to 404")
                    log("log.txt", "sending gmail")
                    send_gmail(gmail_username, gmail_app_password, gmail_to,
                               "Python Stock Alert", f"ERROR url: {i} is invalid")
                    log("log.txt", "gmail sent")
                scorptec_stock[i] = scorptec_result
                write_json("scorptec_stock_json.txt", scorptec_stock)

        if centrecom_urls[0] != "":
            log("log.txt", "centrecom_urls.txt not empty beginning scraping")
            for i in centrecom_urls:
                if centrecom_stock.get(i) is None:
                    centrecom_stock[i] = 0
                    log("log.txt", f"{i} not in dict adding to dict")
                log("log.txt", f"current value in dict is {centrecom_stock.get(i)}")
                log("log.txt", f"getting {i} data")
                centrecom_result = centrecom(i)
                log("log.txt", f"data received response is {centrecom_result}")
                if centrecom_result == 2 and centrecom_stock.get(i) != 2:
                    centrecom_stock[i] = 2
                    log("log.txt", "value in dict changed to 2")
                    log("log.txt", "sending gmail")
                    send_gmail(gmail_username, gmail_app_password, gmail_to, "Python Stock Alert",
                               f" Centrecom Item {i} has Stock Available")
                    log("log.txt", "gmail sent")
                if centrecom_result == 1 and centrecom_stock.get(i) != 1:
                    centrecom_stock[i] = 1
                    log("log.txt", "value in dict changed to 1")
                    log("log.txt", "sending gmail")
                    send_gmail(gmail_username, gmail_app_password, gmail_to, "Python Stock Alert",
                               f"Centrecom Item {i} is Available for Pre-Order")
                    log("log.txt", "gmail sent")
                if centrecom_result == 404 and centrecom_stock.get(i) != 404:
                    centrecom_stock[i] = 404
                    log("log.txt", "value in dict changed to 404")
                    log("log.txt", "sending gmail")
                    send_gmail(gmail_username, gmail_app_password, gmail_to, "Python Stock Alert",
                               f" ERROR url: {i} is invalid")
                    log("log.txt", "gmail sent")
                if centrecom_result == 3 and centrecom_stock.get(i) != 3:
                    centrecom_stock[i] = 3
                    log("log.txt", "value in dict changed to 3")
                    log("log.txt", "sending gmail")
                    send_gmail(gmail_username, gmail_app_password, gmail_to, "Python Stock Alert",
                               f"Centrecom Item {i} is Available In Store")
                    log("log.txt", "gmail sent")
                centrecom_stock[i] = centrecom_result
                write_json("centrecom_stock_json.txt", centrecom_stock)

        if pcpartpicker_urls[0] != "":
            log("log.txt", "pcpartpicker_urls.txt not empty beginning scraping")
            for i in pcpartpicker_urls:
                if pcpartpicker_stock.get(i) is None:
                    pcpartpicker_stock[i] = 0
                    log("log.txt", f"{i} not in dict adding to dict")
                log("log.txt", f"current value in dict is {pcpartpicker_stock.get(i)}")
                log("log.txt", f"getting {i} data")
                pcpartpicker_result = pcpartpicker(i)
                log("log.txt", f"data received response is {pcpartpicker_result}")
                if pcpartpicker_result >= 2 > pcpartpicker_stock.get(i):
                    pcpartpicker_stock[i] = pcpartpicker_result
                    log("log.txt", f"value in dict changed to {pcpartpicker_result}")
                    log("log.txt", "sending gmail")
                    send_gmail(gmail_username, gmail_app_password, gmail_to, "Python Stock Alert",
                               f" PCPartPicker Item {i} is available in {pcpartpicker_result -2 } number of retailers")
                    log("log.txt", "gmail sent")
                if pcpartpicker_result == 1 and pcpartpicker_stock.get(i) != 1:
                    pcpartpicker_stock[i] = 1
                    log("log.txt", "value in dict changed to 1")
                    log("log.txt", "sending gmail")
                    send_gmail(gmail_username, gmail_app_password, gmail_to, "Python Stock Alert",
                               f"PCPartPicker Item {i} is Available for Pre-Order")
                    log("log.txt", "gmail sent")
                if pcpartpicker_result == 404 and pcpartpicker_stock.get(i) != 404:
                    pcpartpicker_stock[i] = 404
                    log("log.txt", "value in dict changed to 404")
                    log("log.txt", "sending gmail")
                    send_gmail(gmail_username, gmail_app_password, gmail_to, "Python Stock Alert",
                               f" ERROR url: {i} is invalid")
                    log("log.txt", "gmail sent")
                pcpartpicker_stock[i] = pcpartpicker_result
                write_json("pcpartpicker_stock_json.txt", pcpartpicker_stock)

        log("log.txt", "Waiting For 30 Seconds before starting loop again")
        time.sleep(30)
        log("log.txt", "Loop end adding 1 to loop start")
        loop_count += 1


if __name__ == '__main__':
    main()
