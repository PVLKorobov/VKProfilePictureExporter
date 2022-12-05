from datetime import datetime


class logger:
    def __init__(self, prefix = ""):
        self.prefix = prefix
        self.log_filename = "activity_log.log"
        self.blank_entry = "[{time}][{prefix}{type}]{message}\n"

# Очистка файла
    def reset_log(self):
        with open(self.log_filename, "w", encoding="utf-8") as log_file:
            log_file.write(f"[Log started at {self._get_current_time()}]\n")

# Получение времени в формате ЧЧ:ММ:СС
    def _get_current_time(self):
        now = datetime.now()
        return now.strftime("%H:%M:%S")

# Логирование состояния программы
    def info(self,message_input):
        entry = self.blank_entry
        current_time = self._get_current_time()
        with open(self.log_filename, "a", encoding="utf-8") as log_file:
            log_file.write(entry.format(time=current_time, type="INFO", message=message_input, prefix=self.prefix))

# Логирование предупреждения
    def warning(self, message_input):
        entry = self.blank_entry
        current_time = self._get_current_time()
        with open(self.log_filename, "a", encoding="utf-8") as log_file:
            log_file.write(entry.format(time=current_time, type="WARNING", message=message_input, prefix=self.prefix))

# Логирование ошибки
    def error(self, message_input):
        entry = self.blank_entry
        current_time = self._get_current_time()
        with open(self.log_filename, "a", encoding="utf-8") as log_file:
            log_file.write(entry.format(time=current_time, type="ERROR", message=message_input, prefix=self.prefix))
        print("Выполнение программы остановлено из-за ошибки. Информация об ошибке в activity_log")
        raise SystemExit(0)