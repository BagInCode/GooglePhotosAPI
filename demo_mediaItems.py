from pprint import pprint
from init_photo_service import service
import pandas as pd


"""
list method
"""
response = service.mediaItems().list(pageSize=25).execute()

lst_medias = response.get("mediaItems")
nextPageToken = response.get("nextPageToken")

while nextPageToken:
    response = service.mediaItems().list(pageSize=25, pageToken=nextPageToken).execute()

    lst_medias.extend(response.get("mediaItems"))
    nextPageToken = response.get("nextPageToken")

df_media_items = pd.DataFrame(lst_medias)


"""
get method
"""
media_id = df_media_items["id"][0]
response = service.mediaItems().get(mediaItemId=media_id).execute()


"""
batchGet method
"""
media_ids = df_media_items["id"][0:2].to_list()
response = service.mediaItems().batchGet(mediaItemIds=media_ids).execute()
print(pd.DataFrame(response.get("mediaItemResults"))["mediaItem"].apply(pd.Series))


"""
search method (by album id)
"""
response_albums_list = service.albums().list().execute()
albums_list = response_albums_list.get("albums")

print(albums_list)

album_id = next(filter(lambda x: "Google Product Icons" in x["title"], albums_list))[
    "id"
]

request_body = {"albumId": album_id, "pageSize": 25}

response_search = service.mediaItems().search(body=request_body).execute()

lstMediaItems = response_search.get("mediaItems")
nextPageToken = response_search.get("nextPageToken")

while nextPageToken:
    request_body["pageToken"] = nextPageToken

    response_search = service.mediaItems().search(body=request_body).execute()
    lstMediaItems.extend(response_search.get("mediaItems"))
    nextPageToken = response_search.get("nextPageToken")

df_search_result = pd.DataFrame(lstMediaItems)


def response_media_items_by_filter(request_body: dict):
    try:
        response_search = service.mediaItems().search(body=request_body).execute()
        lstMediaItems = response_search.get("mediaItems")
        nextPageToken = response_search.get("nextPageToken")

        while nextPageToken:
            request_body["pageToken"] = nextPageToken
            response_search = service.mediaItems().search(body=request_body).execute()

            if not response_search.get("mediaItem") is None:
                lstMediaItems.extend(response_search.get("mediaItems"))
                nextPageToken = response_search.get("nextPageToken")
            else:
                nextPageToken = ""
        return lstMediaItems
    except Exception as e:
        print(e)
        return None


"""
search method (by date)
"""
request_body = {
    "pageSize": 100,
    "filters": {
        "dateFilter": {
            # 'ranges': [
            #     {
            #         'startDate': {
            #             'year': 2019,
            #             'month': 1,
            #             'day': 1
            #         },
            #         'endDate': {
            #             'year': 2019,
            #             'month': 12,
            #             'day': 31
            #         }
            #     }
            # ]
            "dates": [
                {"year": 2019, "month": 12, "day": 23},
                {"year": 2019, "month": 11, "day": 19},
                {"year": 2019, "month": 11, "day": 20},
            ]
        }
    },
}

df_search_result = pd.DataFrame(response_media_items_by_filter(request_body))


"""
search method (content filter)
"""
request_body = {
    "pageSize": 100,
    "filters": {
        "contentFilter": {
            "includedContentCategories": ["LANDMARKS", "GARDENS"],
            "excludedContentCategories": ["SPORT", "ANIMALS"],
        }
    },
}

df_search_result = pd.DataFrame(response_media_items_by_filter(request_body))


"""
search method (media type)
"""
request_body = {
    "pageSize": 100,
    "filters": {"mediaTypeFilter": {"mediaTypes": ["VIDEO"]}},
}

df_search_result = pd.DataFrame(response_media_items_by_filter(request_body))


"""
search method (feature filter)
"""
request_body = {
    "pageSize": 100,
    "filters": {"featureFilter": {"includedFeatures": ["FAVORITES"]}},
}

df_search_result = pd.DataFrame(response_media_items_by_filter(request_body))


"""
search method (includedArchiveMedia, excludedAppCreatedData)
"""
request_body = {
    "pageSize": 100,
    "filters": {"includeArchivedMedia": True, "excludeNonAppCreatedData": False},
}
df_search_result = pd.DataFrame(response_media_items_by_filter(request_body))

"""
batchCretae method
"""
import os
import pickle
import requests

# step 1: Upload byte data to Google Server
image_dir = os.path.join(os.getcwd(), "Images To Upload")
upload_url = "https://photoslibrary.googleapis.com/v1/uploads"
token = pickle.load(open("token_photoslibrary_v1.pickle", "rb"))

headers = {
    "Authorization": "Bearer " + token.token,
    "Content-type": "application/octet-stream",
    "X-Goog-Upload-Protocol": "raw",
}

image_file = os.path.join(image_dir, "Dog_3.jpg")
headers["X-Goog-Upload-File-Name"] = "Dog_the_Shi_Tsu.jpg"

img = open(image_file, "rb").read()
response = requests.post(upload_url, data=img, headers=headers)

request_body = {
    "newMediaItems": [
        {
            "description": "Dog the Shi-tsu",
            "simpleMediaItem": {"uploadToken": response.content.decode("utf-8")},
        }
    ]
}

upload_response = service.mediaItems().batchCreate(body=request_body).execute()


def upload_image(image_path, upload_file_name, token):
    headers = {
        "Authorization": "Bearer " + token.token,
        "Content-type": "application/octet-stream",
        "X-Goog-Upload-Protocol": "raw",
        "X-Goog-File-Name": upload_file_name,
    }

    img = open(image_path, "rb").read()
    response = requests.post(upload_url, data=img, headers=headers)
    print("\nUpload token: {0}".format(response.content.decode("utf-8")))
    return response


tokens = []
image_dir = os.path.join(os.getcwd(), "Images To Upload")
upload_url = "https://photoslibrary.googleapis.com/v1/uploads"
token = pickle.load(open("token_photoslibrary_v1.pickle", "rb"))

image_skytower = os.path.join(image_dir, "Dog_4.jpg")
response = upload_image(image_skytower, "Dog", token)
tokens.append(response.content.decode("utf-8"))

new_media_items = [{"simpleMediaItem": {"uploadToken": tok}} for tok in tokens]

request_body = {"newMediaItems": new_media_items}

upload_response = service.mediaItems().batchCreate(body=request_body).execute()
