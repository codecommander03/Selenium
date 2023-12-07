from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

with open("data.json", "w") as f:
    json.dump([], f)

def write_json(new_data, filename='data.json'):
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data.append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

browser = webdriver.Chrome() # Chrome version 103
browser.get('https://www.amazon.in/s?k=ssd+500gb&crid=3FXBOJL35NOWE&sprefix=ssd+%2Caps%2C232&ref=nb_sb_ss_ts-doa-p_2_4')


isNextDisabled = False

while not isNextDisabled:
    try:
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@data-component-type="s-search-result"]')))

        elem_list = browser.find_element(By.CSS_SELECTOR, "div.s-main-slot.s-result-list.s-search-results.sg-row")

        items = elem_list.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')

        for item in items:
            title = item.find_element(By.TAG_NAME, 'h2').text
            price = "No Price Found"
            img = "No Image Found"
            link = item.find_element(By.CLASS_NAME, 'a-link-normal').get_attribute('href')

            try:
                price = item.find_element(By.CSS_SELECTOR, '.a-price').text.replace("\n", ".")
            except:
                pass

            try:
                img = item.find_element(By.CSS_SELECTOR, '.s-image').get_attribute("src")
            except:
                pass

            print("Title: " + title)
            print("Price: " + price)
            print("Image: " + img)
            print("Link: " + link + "\n")

            write_json({
                "title": title,
                "price": price,
                "image": img,
                "link": link
            })

        next_btn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 's-pagination-next')))

        next_class = next_btn.get_attribute('class')

        if "disabled" in next_class:
            isNextDisabled = True
        else:
            browser.find_element(By.CLASS_NAME, 's-pagination-next').click()

    except Exception as e:
        print(e, "Main Error")
        isNextDisabled = True
