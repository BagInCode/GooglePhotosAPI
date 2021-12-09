import os
from Google import Create_Service

API_NAME = "photoslibrary"
API_VERSION = "v1"
CLIENT_SECRET_FILE = "client_secret_738981472603-0un4c055arekvfvbq5a2d6bv4k30062m.apps.googleusercontent.com.json"
SCOPES = [
    "https://www.googleapis.com/auth/photoslibrary",
    "https://www.googleapis.com/auth/photoslibrary.sharing",
]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
