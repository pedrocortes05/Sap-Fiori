from datetime import date
from cairosvg import svg2png
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

def generate_qr_code(username, password):
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")

    service = Service("/home/pedro/Downloads/chromedriver_linux64/chromedriver")
    service.start()

    driver = webdriver.Remote(service.service_url, options=chrome_options)
    driver.get("https://flpnwc-aj982psom1.dispatcher.us3.hana.ondemand.com/sites/regresoseguro#Shell-home")

    search = driver.find_element(By.ID, "Ecom_User_ID")
    search.send_keys(username)

    search = driver.find_element(By.ID, "Ecom_Password")
    search.send_keys(password)
    search.send_keys(Keys.RETURN)

    #driver.get("https://flpnwc-aj982psom1.dispatcher.us3.hana.ondemand.com/sites/regresoseguro#Shell-home")

    #Click Questionare button
    WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#__tile0-title-inner")))
    driver.find_element(By.CSS_SELECTOR, "#__tile0-title-inner").click()

    #Submit questionare
    #TODO code
    #driver.get("https://flpnwc-aj982psom1.dispatcher.us3.hana.ondemand.com/sites/regresoseguro#Shell-home")

    #Click QR button
    WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#__tile1-subHdr-text")))
    driver.find_element(By.CSS_SELECTOR, "#__tile1-subHdr-text").click()

    #QR SVG
    WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.CSS_SELECTOR, "#__html0")))
    svg_code = driver.find_element(By.CSS_SELECTOR, "#__html0").get_attribute("outerHTML")

    # mm_dd_y
    date_str = date.today().strftime("%m_%d_%y")
    save_path = f"/home/pedro/Documents/Projects/Sap-Fiori/QR-Codes/{date_str}.png"
    svg2png(bytestring=svg_code, write_to=save_path)
