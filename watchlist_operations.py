from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import json
import constants as c
import os
import pandas as pd

def DMA200(company):
    DMA200 = 0.0
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)

    # Go to the screener page
    print(f"\nSCRAPING DATA FOR {company}")
    driver.get(f'{c.BASE_URL}/company/{company}/')

    # Access requests via the `requests` attribute
    company_code = 0
    for request in driver.requests:
        if request.response and request.url[-3::] == '365':
            company_code = int(request.url.split(
                f"{c.BASE_URL}/api/company/")[1].split("/chart/?q=Price-DMA50-DMA200-Volume&days=365")[0])
            print(f"Company code: {company_code}")
            break
    driver.get(
        f'{c.BASE_URL}/api/company/{company_code}/{c.API_QUERY}')
    content = driver.find_element(By.CSS_SELECTOR, "body pre").text
    data = json.loads(content)
    DMA200 = float(data['datasets'][0]['values'][-1][1])
    print(f"DMA200: {DMA200}")
    driver.quit()
    return DMA200


def query(today_file, files_list) -> None:
    os.system('cls')
    DMA200_filter = {}
    # print(today_file)
    df = pd.read_csv(today_file)
    df = df.query(
        'SERIES == "EQ" & CLOSE >= 100 & CLOSE < 1500 & TOTTRDQTY > 50000')
    df.to_csv('output.csv')
    output_path = os.path.abspath('output.csv')
    average_volume = averageVolume(files_list, output_path)
    df.insert(len(df.columns), 'AVGVOL20', value=df['SYMBOL'].map(average_volume))
    df = df.query('TOTTRDQTY > AVGVOL20')

    for index, company in enumerate(df['SYMBOL']):
        print(f"{index+1}/{len(df['SYMBOL'])}")
        dma200 = DMA200(company)
        DMA200_filter[company] = dma200
        os.system('cls')
    # print(DMA200_filter)
    print("Finished calculating average volume of each company for the past 20 days")
    print("Finished scraping DMA200 for each company")

    # df['DMA200'] = df['SYMBOL'].map(DMA200_filter)
    df.insert(len(df.columns), 'DMA200', value=df['SYMBOL'].map(DMA200_filter))
    df = df.query('CLOSE > 0.95*DMA200 & CLOSE < 1.05*DMA200')

    # df = df.query('CLOSE > 1.005*DMA200')
    del_columns = ['ISIN', 'LOW', 'HIGH', 'OPEN', 'PREVCLOSE', 'TIMESTAMP', 'TOTALTRADES', 'TOTTRDVAL']
    for col in del_columns:
            df.pop(item=col)
    os.remove('output.csv')
    df.to_excel('Results.xlsx', index=False)
    

def averageVolume(files_list, output_path):
    average_volume = {}
    today = pd.read_csv(output_path)
    companies = list(today["SYMBOL"])
    for index, file in enumerate(files_list):
        os.system('cls')
        print("Calculating average volume of the past 20 days")
        print(f"{index+1}/{len(files_list)} DONE")
        df = pd.read_csv(file)
        for index, company in enumerate(df['SYMBOL']):
            if company in companies:
                volume = df.loc[df['SYMBOL'] == company, 'TOTTRDQTY'].values[0]
                if company in average_volume:
                    average_volume[company] += volume
                else:
                    average_volume[company] = volume

    else:
        print("Finished calculating average volume of each company for the past 20 days")
        os.system('cls')
        for company in average_volume:
            average_volume[company] = round(
                average_volume[company] / len(files_list), 2)

    return average_volume

