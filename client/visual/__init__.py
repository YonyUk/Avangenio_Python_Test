from .main_view import MainWindow
from core import StringGenerator
from .appconfig import AppConfig

class App:

    def __init__(self,**config):
        self._config = AppConfig(**config)
        pass

    def run(self):
        MainWindow(self._config)
        pass

    pass