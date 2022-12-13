from logger import logger

import requests
import configparser

class VkAPI:
    def __init__(self):
        self.app_id = "51475405"
        self.API_version = "5.131"
        self.base_url = "https://api.vk.com/method/"  # часть url, единая для всех запросов
        
        self.VK_log = logger("VK")
        self.userData = configparser.ConfigParser()
        self.userData.read("user_data.ini")

    # проверка является ли userId символьным именем
    def _isScreenName(self):
        try:
            int(self.userData["VK"]["userId"])
            return False
        except ValueError:
            return True

    # получение числового id пользователя из символьного(ScreenName) userId
    def _getUserId(self):
        requestUrl = "https://api.vk.com/method/users.get"
        headers = {
        "user_ids" : self.userData["VK"]["userId"],
        "access_token" : self.userData["VK"]["token"],
        "v" : 5.131
        }
        self.VK_log.info([f"Отправка запроса users.get по {requestUrl}"])  # logged
        response = requests.get(requestUrl, headers)

        self._raiseForStatus(response.json())

        self.userData["VK"]["userId"] = response.json()["response"][0]["id"]  # Здесь userId присваивается числовое id пользователя.
        self.VK_log.info(["Получено userId из ScreenName"])  # logged

    # проверка кода ответа
    def _raiseForStatus(self, responseData):
        if "error" in responseData:
            error_msg = responseData["error"]["error_msg"]
            error_code = responseData["error"]["error_code"]
            self.VK_log.error(f"{error_msg} error_code:{error_code}")  # logged

    # получение данных о фото профиля
    def _getUnifiedData(self):
        requestUrl = "https://api.vk.com/method/photos.get"
        headers = {
        "owner_id" : self.userData["VK"]["userId"],
        "album_id" : "profile",
        "extended" : 1,
        "access_token" : self.userData["VK"]["token"],
        "v" : 5.131
        }
        self.VK_log.info([f"Отправка запроса photos.get по {requestUrl}"])  # logged
        response = requests.get(requestUrl, headers)

        self._raiseForStatus(response.json())

        index = response.json()["response"]["count"]-1  # индекс последней фотографии в списке
        data = response.json()["response"]["items"][index]
        picUrl = data["sizes"][-1]["url"]
        likesCount = data["likes"]["count"]
        self.VK_log.info([f"Получено url и likesCount фото профиля"])  # logged
        return [picUrl, str(likesCount)]

    # глобальная функция для декомпозиции кода
    def getPfpData(self):
        if self._isScreenName():
            self.VK_log.warning("Вместо userId получено ScreenName")  # logged
            self._getUserId()  # Здесь userId является символным ScreenName, а не числовым id.
            return self._getUnifiedData()
        else:
            return self._getUnifiedData()