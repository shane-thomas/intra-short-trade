from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import json
import constants as c

def DMA200(company):
    DMA200 = 0.0

    # Create a new instance of the driver
    print("\nCREATING BROWSER INSTANCE")

    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    # Go to the screener page
    print(f"\nSCRAPING DATA FOR {company}")
    driver.get(f'{c.BASE_URL}/company/{company}/')

    # Access requests via the `requests` attribute
    
    for request in driver.requests:
        if request.response and request.url[-3::] == '365':
            company_code = request.url[36:40]
            print(company_code)
            break
    driver.get(
        f'{c.BASE_URL}/api/company/{company_code}/{c.API_QUERY}')
    content = (driver.find_element(By.CSS_SELECTOR, "body pre").text)
    data = json.loads(content)
    
    DMA200 = data['datasets'][0]['values'][0][1]
    print(DMA200)
    driver.quit()
    return DMA200


if __name__ == "__main__":
    DMA200('INFY')
