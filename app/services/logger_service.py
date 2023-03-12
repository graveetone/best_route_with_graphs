from services.config_service import ConfigService
class Loger:
    @staticmethod
    def log(message, *args):
        if ConfigService.LOGGER_ENABLED:
            print(f"{message}: {args}")