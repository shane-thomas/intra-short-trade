from seleniumwire import webdriver  # Import from seleniumwire
from selenium.webdriver.common.by import By
import constants as c

def DMA200(company):
    DMA200 = 0.0

    # Create a new instance of the driver
    print("\nCREATING BROWSER INSTANCE")
    options = webdriver.EdgeOptions()
    options.add_argument("--log-level=3")
    driver = webdriver.Edge(options=options)

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
    DMA200 = float(driver.find_element(
        By.CSS_SELECTOR, "body > div.cm-editor.ͼ1.ͼ3.ͼ4.ͼ6.ͼ5 > div.cm-scroller > div.cm-content.cm-lineWrapping > div:nth-child(9) > span").text[1:-1])
    print(DMA200)
    driver.quit()
    return DMA200


if __name__ == "__main__":
    DMA200('INFY')