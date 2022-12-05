# Экспортер фото профиля пользователя
## Получение необходимых данных
Пользователь вручную вводит токен доступа Яндекс.Диска и id пользователя ВКонтакте.  
Сервисный ключ доступа вашего приложения ВКонтакте бессрочен, а потому единожды записывается в файл vk_token для дальнейшего считывания программой.

## Работа программы
Через VKAPI скрипт получает ссылку URL на фото профиля пользователя в наибольшем возможном разрешении и количетсво лайков.  
Через API Яндекс.Диска фото загружается по URL на в автоматически созданную директорию на Яндекс.Диске. В качестве имени используется количество лайков. (прим. 51.jpg) После чего данные об экспортированном фото сохраняются в json файл photo_data в виде

{  
    "filename" : {имя файла},  
    "size" : {тип размера файла}  
}

В случае, если фото с такии именем уже существует на Диске, оно не будет загружено, и информация о дубликате не появится в json файле.

Процесс выполнения программы логируется в файл activity_log, включая критические ошибки, не позволяющие продолжить выполнение кода программы.

Список необходимых зависимостей находится в requirements.txt
