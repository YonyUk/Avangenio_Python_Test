import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from core import StringGenerator,writefile
from visual.appconfig import AppConfig
from tkinter import messagebox
from threading import Thread,Lock
import time

class MainWindow(tk.Tk):

    _writing = False
    _process = None
    _progress_bar = None
    _lock = Lock()
    _strings = ''

    def __init__(self,config:AppConfig,*args,**kwargs):
        super().__init__(*args,**kwargs)
        Thread(target=lambda:self._check_writing_process(),daemon=True).start()
        self._generator = config.Generator
        self.geometry(config.size if config.size != None else '800x600')
        self.title('MainView')
        self.protocol('WM_DELETE_WINDOW',lambda:self._on_close())

        # container for the params controls
        self._params_box = tk.Frame(self)
        self._params_box.pack(side=tk.TOP,pady=50)

        # container for the count of lines to write in the file
        self._string_lines_count_input_box = tk.Frame(self._params_box)
        self._string_lines_count_input_box.pack(side=tk.LEFT,padx=30)

        # lines
        self._lines_count = tk.IntVar(self._string_lines_count_input_box)
        self._lines_count.set(1000000)
        self._string_input_label = tk.Label(self._string_lines_count_input_box,text='Lines')
        self._string_input_label.pack(side=tk.TOP)
        self._string_count_input = tk.Spinbox(
            self._string_lines_count_input_box,
            from_=config.min_lines if config.min_lines != None else 10,
            to=config.max_lines if config.max_lines != None else 2000000,
            increment=config.lines_increment if config.lines_increment != None else 1000,
            textvariable=self._lines_count
        )
        self._string_count_input.pack(side=tk.BOTTOM)

        # container for the min count of characters
        self._min_chars_count_input_box = tk.Frame(self._params_box)
        self._min_chars_count_input_box.pack(side=tk.LEFT,padx=30)

        # min count characters
        self._min_chars_count = tk.IntVar(self._min_chars_count_input_box)
        self._min_chars_count.set(50)
        self._min_char_count_label = tk.Label(self._min_chars_count_input_box,text='Min count characters')
        self._min_char_count_label.pack(side=tk.TOP)
        self._min_chars_count_input = tk.Spinbox(
            self._min_chars_count_input_box,
            from_=config.min_chars if config.min_chars != None else 10,
            to=config.max_chars if config.max_chars != None else 1000,
            increment=config.chars_increment if config.chars_increment != None else 10,
            textvariable=self._min_chars_count
        )
        self._min_chars_count_input.pack(side=tk.BOTTOM)

        # container for the max count of characters
        self._max_chars_count_input_box = tk.Frame(self._params_box)
        self._max_chars_count_input_box.pack(side=tk.LEFT,padx=30)

        # max count characters
        self._max_chars_count = tk.IntVar(self._max_chars_count_input_box)
        self._max_chars_count.set(50)
        self._max_chars_count_label = tk.Label(self._max_chars_count_input_box,text='Max count characters')
        self._max_chars_count_label.pack(side=tk.TOP)
        self._max_chars_count_input = tk.Spinbox(
            self._max_chars_count_input_box,
            from_=config.min_chars if config.min_chars != None else 10,
            to=config.max_chars if config.max_chars != None else 1000,
            increment=config.chars_increment if config.chars_increment != None else 10,
            textvariable=self._max_chars_count
        )
        self._max_chars_count_input.pack(side=tk.BOTTOM,padx=30)

        self._buttons_box = tk.Frame(self)
        self._buttons_box.pack(side=tk.BOTTOM,pady=50)

        self._file_generator_btn = tk.Button(self._buttons_box,text='generate random file',command=lambda:self._save_file())
        self._file_creator_btn = tk.Button(self._buttons_box,text='manually cration',command=lambda:print('ok'))

        self._file_generator_btn.pack(side=tk.LEFT,pady=10,padx=10)
        self._file_creator_btn.pack(side=tk.RIGHT,pady=10,padx=10)

        self.mainloop()

        pass

    def _save_file(self,path=''):
        if not self._validate_params():
            messagebox.showerror('Invalid arguments','<Min chars count> must be less than <Max chars count>')
            pass
        else:
            self._generator.min_length = self._min_chars_count.get()
            self._generator.max_length = self._max_chars_count.get()
            file = filedialog.asksaveasfilename()
            self._progress_bar = ttk.Progressbar(
                self,
                orient=tk.HORIZONTAL,
                mode='determinate',
                length=300,
                maximum=self._lines_count.get()
            )   
            self._progress_bar.pack(side=tk.TOP)
            self._process = Thread(target=lambda:self._write_strings(file),daemon=True)
            self._process.start()
            pass
        pass

    def _validate_params(self):
        return self._min_chars_count.get() < self._max_chars_count.get()

    def _generate_strings(self,count:int):
        print('hebra comenzada')
        text = ''
        for string in self._generator.GenerateStrings(count):
            text += string + '\n'
            pass
        print('hebra terminada')
        self._lock.acquire()
        self._strings += text
        self._lock.release()
        

    def _write_strings(self,file:str):
        self._writing = True
        text = ''
        threads = []
        for _ in range(self._lines_count.get() // 10000):
            threads.append(Thread(target=lambda:self._generate_strings(10000),daemon=True))
            pass
        threads.append(Thread(target=lambda:self._generate_strings(self._lines_count.get() - (self._lines_count.get() // 10000) * 10000)))
        for t in threads:
            t.start()
            pass

        for t in threads:
            t.join()
            pass

            # if self._progress_bar != None:
                #     self._progress_bar.step(1)
            #     pass
        text = text[:len(text) - 1]
        writefile(file,text)
        self._writing = False
        self._progress_bar.destroy()
        self._progress_bar = None
        pass

    def _check_writing_process(self):
        while True:
            if self._process != None and not self._process.is_alive():
                self._process.join()
                self._process = None
                pass
            time.sleep(1)
            pass
        pass

    def _on_close(self):
        if self._writing:
            if messagebox.askyesno('Salir','Desea detener el proceso de escritura?'):
                if self._progress_bar != None:
                    self._progress_bar.destroy()
                    self._progress_bar = None
                    pass
                self.destroy()
                pass
            pass
        else:
            self.destroy()
            pass
        pass

    pass