from logger import logger
from API.VkAPI import VkAPI
from API.YanDiskAPI import YandexAPI
import json


main_log = logger("main - ")
main_log.reset_log()

userId = input("Введите id пользователя ВКонтакте: ")
YDToken = input("Введите токен с Полигона Яндекс.Диска: ")
VKToken = ""
with open("vk_token.txt") as tokenFile:
    YDToken = tokenFile.readline()
main_log.info(f"Получено id пользователя {userId}") #logged
main_log.info("Получен токен доступа ВКотнакте") #logged
main_log.info("Получен токен доступа Яндекс.Диска") #logged

VK_API = VkAPI(userId, VKToken)
PfpData = VK_API.getPfpData()
filename = PfpData[1]+".jpg"

YD_API = YandexAPI(YDToken)
uploaded = YD_API.upload_by_url(PfpData[0], filename)

# Запись данных о фото в json файл
fileData = []
if uploaded:
    # Считывается уже имеющиеся в файле данные
    with open("photo_data.json", "r") as dataFile:
        fileData = json.load(dataFile)
        fileData.append({
            "file_name" : filename,
            "size" : "z"
        })
    # В файл записываются расширенные данные
    with open("photo_data.json", "w") as dataFile:
        json.dump(fileData, dataFile, indent=4)
        main_log.info("Данные о фото сохранены в json файл") #logged