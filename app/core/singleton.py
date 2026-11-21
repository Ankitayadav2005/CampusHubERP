class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]


class AppConfig(metaclass=SingletonMeta):

    def __init__(self):
        self.app_name = "CampusHub ERP"
        self.version = "1.0"


config1 = AppConfig()
config2 = AppConfig()

print("Application Name:", config1.app_name)
print("Version:", config1.version)

print("Same Object:", config1 is config2)