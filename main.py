from logger import logger
from API.VkAPI import VkAPI
from API.YanDiskAPI import YandexAPI

import json
import configparser

def getUserData():
    userData["VK"]["userId"] = input("Введите id пользователя ВКонтакте: ")
    userData["YD"]["token"] = input("Введите токен с Полигона Яндекс.Диска: ")
    main_log.info([f"Получен id пользователя", 
                    "Получен токен доступа Яндекс.Диска"])  # logged

    
if __name__ == "__main__":


    userData = configparser.ConfigParser()
    userData.read("user_data.ini")
    main_log = logger("main")
    main_log.info(["Инициальзован обьект класса logger",
                   "Инициализирован обьект класса ConfigParser"])  # logged

    main_log.reset_log()


    YD_API = YandexAPI()
    VK_API = VkAPI()
    main_log.info([f"Инициальзован обьект класса YandexAPI", 
                   f"Инициализован обьект класса VkAPI"])  # logged


    PfpData = VK_API.getPfpData()
    main_log.info([f"Получены данные фотографии PfpData={PfpData}"])
    picUrl = PfpData[0]
    savedCount = int(input("Сколько изображений необходимо сохранить?: "))
    filename = PfpData[1]
    uploaded = YD_API.uploadByURL(picUrl, filename, savedCount)  # bool: true - файл успешно загружен на Я.Диск

    # запись данных о фото в json файл
    fileData = []
    if uploaded:
        # Считываются уже имеющиеся в файле данные.
        with open("photo_data.json", "r") as dataFile:
            fileData = json.load(dataFile)
            fileData.append({
                "file_name" : filename,
                "size" : "z"
            })
        # В файл записываются расширенные данные.
        with open("photo_data.json", "w") as dataFile:
            json.dump(fileData, dataFile, indent=4)
            main_log.info(["Данные о фото сохранены в json файл"])  # logged