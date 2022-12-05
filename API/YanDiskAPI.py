from logger import logger
import requests


class YandexAPI:
    def __init__(self, token):
        self.token = token
        self.path_name = "Exported Profile Pictures"
        self.base_headers = {"Content-Type": "application/json", 
                            "Authorization": f"OAuth {self.token}"}
                            # Стандартный набор аргументов запроса
        self.base_url = "https://cloud-api.yandex.net/v1/disk/" # Часть url, единая для всех запросов
        self.YD_log = logger("YD - ")
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
    
# Проверка кода ответа
    def _raiseForStatus(self, responseCode):
        if responseCode in self.YD_error_codes:
            error_msg = self.YD_error_codes[responseCode]
            self.YD_log.error(f"{error_msg} error_code:{responseCode}") #logged

# Поиск на Я.Диске дубликатов экспортируемого файла
    def _check_for_duplicate(self, filename):
        request_url = self.base_url + "resources"
        headers = self.base_headers
        params = {"path" : self.path_name, "fields" : "items"}
        self.YD_log.info(f"Отправка запроса get по {request_url}") #logged
        response = requests.get(request_url, headers=headers, params=params)

        self._raiseForStatus(response.status_code)

        embedded_items = response.json()["_embedded"]["items"]
        for item in embedded_items:
            if item["name"] == filename:
                self.YD_log.warning(f"Файл '{filename}' уже существует на Диске") #logged
                return False
        self.YD_log.info(f"Файл '{filename}' не существует на Диске") #logged
        return True

# Загрузка файла на Я.диск по URL ресурса
    def upload_by_url(self, file_url, filename):
        self._create_folder()
        if self._check_for_duplicate(filename):
            request_url = self.base_url + "resources/upload"
            headers = self.base_headers
            params = {"path" : f"{self.path_name}/" + filename, "url" : file_url}
            self.YD_log.info(f"Отправка запроса post по {request_url}") #logged
            response = requests.post(request_url, headers=headers, params=params)

            self._raiseForStatus(response.status_code)

            if response.status_code == 202:
                self.YD_log.info(f"Файл '{filename}' загружен на Диск") #logged
                return True
        else:
            self.YD_log.info(f"Файл '{filename}' не был загружен на Диск, так как уже существует") #logged
            return False

# Создание папки для файлов на Я.Диске
    def _create_folder(self):
        request_url = self.base_url + "resources"
        headers = self.base_headers
        params = {"path" : self.path_name}
        self.YD_log.info(f"Отправка запроса put по {request_url}") #logged
        response = requests.put(request_url, headers=headers, params=params)

        self._raiseForStatus(response.status_code)

        if response.status_code == 201:
            self.YD_log.info(f"Создана директория {self.path_name}") #logged
        elif response.status_code == 409:
            self.YD_log.warning(f"Директория {self.path_name} уже существует") #logged