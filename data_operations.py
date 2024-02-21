from zipfile import ZipFile
from datetime import datetime, timedelta
import requests
import os
import constants as c


def get_file(date):
    url = f"{c.FILE_URL}{date.strftime('%Y')}/{date.strftime('%b').upper()}"
    date_str = date.strftime("%d%b%Y").upper()
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
    today_file_path = os.path.abspath(filename[0:-4])

    return today_file_path


def download_files():
    directory = os.getcwd()  # Get current working directory

    # Delete old existing .csv files
    csv_files = [f for f in os.listdir(directory) if (f.endswith(".csv") or f.endswith(".zip"))]
    for f in csv_files:
        os.remove(os.path.join(directory, f))

    today = datetime.today()  # Get today's date
    date_range = []
    today_file = ""
    files_list = []

    current_date = today
    index = 0
    while index < 20:
        os.system('cls')
        print(f"{index+1}/20")

        if current_date.weekday() < 5:  # Check if the current date is a weekday (Monday to Friday)
            date_range.append(current_date)
            try:  # Download file for that particular date if it isn't a holiday
                file_path = get_file(current_date)
                files_list.append(file_path)
                if index == 0:
                    today_file = file_path
                index += 1
            except Exception as e:
                print(f"Error getting file for date {current_date}: {e}")
        current_date -= timedelta(days=1)  # Move to the previous day

    # Remove any redundant .zip files of possible holidays
    zip_files = [f for f in os.listdir(directory) if (f.endswith(".zip"))]
    for f in zip_files:
        os.remove(os.path.join(directory, f))
    return [files_list, today_file]


if __name__ == "__main__":
    print(download_files())
