# Экспортер фото профиля пользователя
## Получение необходимых данных
Пользователь вручную вводит токен доступа Яндекс.Диска и id или Screen Name пользователя ВКонтакте.  
Сервисный ключ доступа приложения ВКонтакте бессрочен, а потому записывается в файл **user_data.ini** для дальнейшего считывания программой. В случае обновления сервисного токена приложения, просто замените старый токен на новый в том же файле **user_data.ini**  
### *Важно*
*Токен должен быть записан в файл под заголовком* `["VK"]`  
***Пример:*** `token=your_token`

## Работа программы
Через VKAPI скрипт получает ссылку URL на фото профиля пользователя в наибольшем возможном разрешении и количетсво лайков.  
Через API Яндекс.Диска фото загружается по URL на в автоматически созданную директорию на Яндекс.Диске. Пользователь вводит количество копий фото, которые будут сохранены. *Каждая копия будет пронумерована начиная с 1*. В качестве имени используется количество лайков. (прим. 51.jpg) После чего данные об экспортированном фото сохраняются в json файл photo_data в виде  
```
{  
    "filename" : {имя файла},  
    "size" : {тип размера файла}  
}
``` 
В случае, если фото с такии именем уже существует на Диске, оно не будет загружено, и информация о дубликате не появится в json файле.

Процесс выполнения программы логируется в файл **activity_log**, включая критические ошибки, не позволяющие продолжить выполнение кода программы.

Список необходимых зависимостей находится в **requirements.txt**
