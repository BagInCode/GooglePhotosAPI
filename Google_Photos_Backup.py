import os
from Google import Create_Service
import pandas as pd  # pip install pandas
import requests  # pip install requests

pd.set_option("display.max_columns", 100)
pd.set_option("display.max_rows", 150)
pd.set_option("display.max_colwidth", 150)
pd.set_option("display.width", 150)
pd.set_option("expand_frame_repr", True)

CLIENT_SECRET_FILE = "client_secret_738981472603-0un4c055arekvfvbq5a2d6bv4k30062m.apps.googleusercontent.com.json"
API_NAME = "photoslibrary"
API_VERSION = "v1"
SCOPES = ["https://www.googleapis.com/auth/photoslibrary"]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

myAblums = service.albums().list().execute()
myAblums_list = myAblums.get("albums")
dfAlbums = pd.DataFrame(myAblums_list)
travel_album_id = (
    dfAlbums[dfAlbums["title"] == "Dog"]["id"].to_string(index=False).strip()
)


def download_file(url: str, destination_folder: str, file_name: str):
    response = requests.get(url)
    if response.status_code == 200:
        print("Downloading file {0}".format(file_name))
        with open(os.path.join(destination_folder, file_name), "wb") as f:
            f.write(response.content)
            f.close()


media_files = (
    service.mediaItems()
    .search(body={"albumId": travel_album_id})
    .execute()["mediaItems"]
)

destination_folder = r".\Photos Backup"

for media_file in media_files:
    file_name = media_file["filename"]
    download_url = media_file["baseUrl"] + "=d"
    download_file(download_url, destination_folder, file_name)
