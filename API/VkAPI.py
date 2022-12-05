from logger import logger
import requests

class VkAPI:
    def __init__(self, userId, token):
        self.userId = userId
        self.token = token
        self.app_id = "51475405"
        self.API_version = "5.131"
        self.base_url = "https://api.vk.com/method/" # Часть url, единая для всех запросов
        self.VK_log = logger("VK - ")

    # Проверка кода ответа
    def _raiseForStatus(self, responseData):
        if "error" in responseData:
            error_msg = responseData["error"]["error_msg"]
            error_code = responseData["error"]["error_code"]
            self.VK_log.error(f"{error_msg} error_code:{error_code}") #logged

    # Получение данных о фото профиля
    def getPfpData(self):
        requestUrl = "https://api.vk.com/method/photos.get"
        headers = {
        "owner_id" : self.userId,
        "album_id" : "profile",
        "extended" : 1,
        # "rev" : 1,
        "access_token" : self.token,
        "v" : 5.131
        }
        self.VK_log.info(f"Отправка запроса photos.get по {requestUrl}") #logged
        response = requests.get(requestUrl, headers)

        self._raiseForStatus(response.json())

        index = response.json()["response"]["count"]-1 # Индекс последней фотографии в списке
        data = response.json()["response"]["items"][index]
        picUrl = data["sizes"][-1]["url"]
        likesCount = data["likes"]["count"]
        self.VK_log.info(f"Получено url и likesCount фото профиля") #logged
        return [picUrl, str(likesCount)]