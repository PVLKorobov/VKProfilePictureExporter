from logger import logger
from API.VkAPI import VkAPI
from API.YanDiskAPI import YandexAPI

import json

def getUserData():
    userId = input("Введите id пользователя ВКонтакте: ")
    YDToken = input("Введите токен с Полигона Яндекс.Диска: ")
    VKToken = ""
    with open("vk_token.txt") as tokenFile:
        VKToken = tokenFile.readline()
    main_log.info([f"Получено id пользователя {userId}", 
                    "Получен токен доступа ВКотнакте", 
                    "Получен токен доступа Яндекс.Диска"])  # logged

    return [YDToken, VKToken, userId]

    
if __name__ == "__main__":


    main_log = logger("main")
    main_log.info(["Инициальзован обьект класса logger"])  # logged

    main_log.reset_log()
    userData = getUserData()
    # 0 - YDToken; 1 - VKToken; 2 - userId


    YD_API = YandexAPI(userData[0])
    VK_API = VkAPI(userData[2], userData[1])
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