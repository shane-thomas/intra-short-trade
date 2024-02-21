from data_operations import *
from watchlist_operations import *

if __name__ == "__main__":
    downloaded_files = download_files()
    files_list = downloaded_files[0]
    latest_bhavcopy = downloaded_files[1]
    query(latest_bhavcopy, files_list)
    print("Final shortlisted companies are listed in Results.xlsx")


