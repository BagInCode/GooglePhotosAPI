from init_photo_service import service
import pandas as pd

"""
list method
"""
response = service.albums().list(pageSize=50, excludeNonAppCreatedData=False).execute()

lstAlbums = response.get("albums")
nextPageToken = response.get("nextPageToken")

while nextPageToken:
    response = service.albums.list(
        pageSize=50, excludeNonAppCreatedData=False, pageToken=nextPageToken
    )
    lstAlbums.append(response.get("ablums"))
    nextPageToken = response.get("nextPageToken")

df_albums = pd.DataFrame(lstAlbums)


"""
get method
"""
my_album_id = df_albums[df_albums["title"] == "Dog"]["id"][0]
response = service.albums().get(albumId=my_album_id).execute()
print(response)


"""
create method
"""
request_body = {"album": {"title": "My Family Photos"}}
response_album_family_photos = service.albums().create(body=request_body).execute()


"""
addEnrichment (album description)
"""
request_body = {
    "newEnrichmentItem": {"textEnrichment": {"text": "This is my family album"}},
    "albumPosition": {"position": "LAST_IN_ALBUM"},
}

response = (
    service.albums()
    .addEnrichment(albumId=response_album_family_photos.get("id"), body=request_body)
    .execute()
)


"""
addEnrichment (album location aka map)
"""
request_body = {
    "newEnrichmentItem": {
        "locationEnrichment": {
            "location": {
                "locationName": "Kyiv, UA",
                "latlng": {"latitude": 50.45466, "longitude": 30.5238},
            }
        }
    },
    "albumPosition": {"position": "LAST_IN_ALBUM"},
}
response = (
    service.albums()
    .addEnrichment(albumId=response_album_family_photos.get("id"), body=request_body)
    .execute()
)


"""
addEnrichment (album map route)
"""
request_body = {
    "newEnrichmentItem": {
        "mapEnrichment": {
            "origin": {
                "locationName": "Kyiv, UA",
                "latlng": {"latitude": 50.45466, "longitude": 30.5238},
            },
            "destination": {
                "locationName": "Kremenchuk, UA",
                "latlng": {"latitude": 49.06802, "longitude": 33.42041},
            },
        }
    },
    "albumPosition": {"position": "FIRST_IN_ALBUM"},
}

response = (
    service.albums()
    .addEnrichment(albumId=response_album_family_photos.get("id"), body=request_body)
    .execute()
)


"""
Share and unshare methods
"""
request_body = {"sharedAlbumOptions": {"isCollaborative": True, "isCommentable": True}}
response = (
    service.albums()
    .share(albumId=response_album_family_photos["id"], body=request_body)
    .execute()
)


service.albums().unshare(albumId=response_album_family_photos.get("id")).execute()
