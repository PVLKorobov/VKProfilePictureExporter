from logger import logger

import requests
import configparser


class YandexAPI:
    def __init__(self):
        self.path_name = "Exported Profile Pictures"
        self.base_url = "https://cloud-api.yandex.net/v1/disk/"  # часть url, единая для всех запросов

        self.userData = configparser.ConfigParser()
        self.userData.read("user_data.ini")
        self.YD_log = logger("YD")
        self.YD_error_codes = {400:"Некорректные данные.",
                            401:"Не авторизован.",
                            403:"API недоступно. Ваши файлы занимают больше места, чем у вас есть.",
                            404:"Не удалось найти запрошенный ресурс.",
                            406:"Ресурс не может быть представлен в запрошенном формате.",
                            413:"Загрузка файла недоступна. Файл слишком большой.",
                            423:"Технические работы. Сейчас можно только просматривать и скачивать файлы.",
                            429:"Слишком много запросов.",
                            503:"Сервис временно недоступен.",
                            507:"Недостаточно свободного места."}
    
# проверка кода ответа
    def _raiseForStatus(self, responseCode):
        if responseCode in self.YD_error_codes:
            error_msg = self.YD_error_codes[responseCode]
            self.YD_log.error(f"{error_msg} error_code:{responseCode}")  # logged

# поиск на Я.Диске дубликатов экспортируемого файла
    def _checkForDuplicate(self, filename):
        request_url = self.base_url + "resources"
        headers = {"Content-Type": "application/json", 
                   "Authorization": "OAuth {token}".format(token=self.userData["YD"]["token"])}
        params = {"path" : self.path_name, "fields" : "items"}
        self.YD_log.info([f"Отправка запроса get по {request_url}"])  # logged
        response = requests.get(request_url, headers=headers, params=params)

        self._raiseForStatus(response.status_code)

        embedded_items = response.json()["_embedded"]["items"]
        for item in embedded_items:
            if item["name"] == filename:
                self.YD_log.warning(f"Файл '{filename}' уже существует на Диске")  # logged
                return False
        self.YD_log.info([f"Файл '{filename}' не существует на Диске"])  # logged
        return True

# загрузка файла на Я.диск по URL ресурса
    def uploadByURL(self, file_url, filename, savedCount):
        self._createFolder()
        if savedCount > 1:
            self.YD_log.info([f"Сохранение {savedCount} файлов на Диск"])  # logged
            filename += "({index}).jpg"
            if self._checkForDuplicate(filename.format(index=1)):
                for i in range(1, savedCount + 1):
                        request_url = self.base_url + "resources/upload"
                        headers = {"Content-Type": "application/json", 
                                   "Authorization": "OAuth {token}".format(token=self.userData["YD"]["token"])}
                        params = {"path" : f"{self.path_name}/" + filename.format(index=i), "url" : file_url}
                        self.YD_log.info([f"Отправка запроса post по {request_url}"])  # logged
                        response = requests.post(request_url, headers=headers, params=params)

                        self._raiseForStatus(response.status_code)

                        if response.status_code == 202:
                            self.YD_log.info([f"Файл '{filename.format(index=i)}' загружен на Диск"])  # logged
                self.YD_log.info([f"{savedCount} файлов сохранено на Диск"])  # logged
                return True
            else:
                self.YD_log.info([f"Файл '{filename}' не был загружен на Диск, так как уже существует"])  # logged
                return False
            
        else:
            filename += ".jpg"
            if self._checkForDuplicate(filename):
                request_url = self.base_url + "resources/upload"
                headers = {"Content-Type": "application/json", 
                           "Authorization": "OAuth {token}".format(token=self.userData["YD"]["token"])}
                params = {"path" : f"{self.path_name}/" + filename, "url" : file_url}
                self.YD_log.info([f"Отправка запроса post по {request_url}"])  # logged
                response = requests.post(request_url, headers=headers, params=params)

                self._raiseForStatus(response.status_code)

                if response.status_code == 202:
                    self.YD_log.info([f"Файл '{filename}' загружен на Диск"])  # logged
                    return True
            else:
                self.YD_log.info([f"Файл '{filename}' не был загружен на Диск, так как уже существует"])  # logged
                return False
# Не придумал как вынести код в другую функцию, чтобы избежать повторения.
# Потому здесь два схожих блока кода.


# создание папки для файлов на Я.Диске
    def _createFolder(self):
        request_url = self.base_url + "resources"
        headers = {"Content-Type": "application/json", 
                   "Authorization": "OAuth {token}".format(token=self.userData["YD"]["token"])}
        params = {"path" : self.path_name}
        self.YD_log.info([f"Отправка запроса put по {request_url}"])  # logged
        response = requests.put(request_url, headers=headers, params=params)

        self._raiseForStatus(response.status_code)

        if response.status_code == 201:
            self.YD_log.info([f"Создана директория {self.path_name}"])  # logged
        elif response.status_code == 409:
            self.YD_log.warning(f"Директория {self.path_name} уже существует")  # logged