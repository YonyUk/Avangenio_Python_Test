from .main_view import MainWindow
from core import StringGenerator
from .appconfig import AppConfig

class App:
    '''
    app class
    '''
    def __init__(self,**config):
        self._config = AppConfig(**config['app'])
        pass

    def run(self):
        '''
        run the app
        '''
        MainWindow(self._config)
        pass

    pass