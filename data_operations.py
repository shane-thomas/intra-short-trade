from zipfile import ZipFile
from datetime import datetime
import requests
import os
import constants as c


def get_today_file():
    # Get today's date
    today = datetime.today()
    url = f"{c.FILE_URL}{today.strftime('%Y')}/{today.strftime('%b').upper()}"
    date_str = today.strftime("%d%b%Y").upper()
    filename = "cm{}bhav.csv.zip".format(date_str)

    # GET Request to URL for downloading the file
    url = "{}/{}".format(url, filename)
    response = requests.get(url)

    # Saving file locally
    with open(f"{filename}", 'wb') as f:
        f.write(response.content)

    # Extracting local zip file
    with ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall()
    os.remove(filename)


if __name__ == "__main__":
    get_today_file()
