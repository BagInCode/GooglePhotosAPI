import sys, pickle, os, io

if hasattr(sys, "frozen"):
    os.environ["PATH"] = sys._MEIPASS + ";" + os.environ["PATH"]
from MyWidgets import ListboxWidget
import requests
from Google import Create_Service
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    qApp,
    QDesktopWidget,
    QListWidget,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont, QIcon


class GooglePhotos:
    upload_base_url = "https://photoslibrary.googleapis.com/v1/uploads"
    API_NAME = "photoslibrary"
    API_VERSION = "v1"
    CLIENT_SECRET_FILE = "client_secret_738981472603-0un4c055arekvfvbq5a2d6bv4k30062m.apps.googleusercontent.com.json"
    SCOPES = [
        "https://www.googleapis.com/auth/photoslibrary",
        "https://www.googleapis.com/auth/photoslibrary.sharing",
    ]

    def __init__(self):
        self.initService()

    def initService(self):
        self.service = Create_Service(
            GooglePhotos.CLIENT_SECRET_FILE,
            GooglePhotos.API_NAME,
            GooglePhotos.API_VERSION,
            GooglePhotos.SCOPES,
        )
        self.client_token = pickle.load(open("token_photoslibrary_v1.pickle", "rb"))

    def upload_image(self, image_path):
        try:
            file_base_name = os.path.basename(image_path)
            headers = {
                "Authorization": "Bearer " + self.client_token.token,
                "Content-type": "application/octet-stream",
                "X-Goog-Upload-Protocol": "raw",
                "X-Goog-File-Name": file_base_name,
            }
            image_data = open(image_path, "rb").read()
            response_upload = requests.post(
                GooglePhotos.upload_base_url, headers=headers, data=image_data
            )
            print(response_upload.content.decode("utf-8"))
            return response_upload.content.decode("utf-8")
        except Exception as e:
            print(e)
            return None


class GooglePhotoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Google Photos Uploader")
        self.setWindowIcon(QIcon(r"<icon path>"))
        self.resize(1200, 800)
        self.centerWindow()
        self.initGooglePhotos()

        buttonFont = QFont("Open Sans", 12, QFont.Bold)

        # Buttons Layout
        self.mainLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()
        buttonLayout.setAlignment(Qt.AlignRight)

        # Listbox Layout
        self.listbox = ListboxWidget()

        # create buttons
        button_upload = QPushButton("&Upload")
        button_upload.setFixedSize(200, 50)
        button_upload.setFont(buttonFont)

        button_remove = QPushButton("&Remove")
        button_remove.setFixedSize(200, 50)
        button_remove.setFont(buttonFont)

        button_close = QPushButton("&Close")
        button_close.setFixedSize(200, 50)
        button_close.setFont(buttonFont)

        buttonLayout.addWidget(button_upload)
        buttonLayout.addWidget(button_remove)
        buttonLayout.addWidget(button_close)

        button_upload.clicked.connect(self.uploate_photos)
        button_remove.clicked.connect(self.remove_listbox_selection)
        button_close.clicked.connect(qApp.quit)

        self.mainLayout.addWidget(
            QLabel("<font size=5>Drag and drop your photos here </font")
        )
        self.mainLayout.addWidget(self.listbox)
        self.mainLayout.addLayout(buttonLayout)
        self.setLayout(self.mainLayout)

    def centerWindow(self):
        centerPoint = QDesktopWidget().availableGeometry().center()

        qr = self.frameGeometry()
        qr.moveCenter(centerPoint)
        self.move(qr.topLeft())

    def uploate_photos(self):
        tokens = []
        if self.listbox.count() > 0:
            for i in range(self.listbox.count() - 1, -1, -1):
                image_token = self.gp.upload_image(self.listbox.item(i).text())
                tokens.append(image_token)
                self.listbox.takeItem(i)

        new_media_items = [{"simpleMediaItem": {"uploadToken": tok}} for tok in tokens]
        request_body = {"newMediaItems": new_media_items}
        self.gp.service.mediaItems().batchCreate(body=request_body).execute()
        print("Photos ploaded")

    def remove_listbox_selection(self):
        self.listbox.takeItem(self.listbox.currentRow())

    def initGooglePhotos(self):
        self.gp = GooglePhotos()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    PhootApp = GooglePhotoApp()
    PhootApp.show()

    sys.exit(app.exec_())
