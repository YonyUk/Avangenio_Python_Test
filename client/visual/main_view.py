import tkinter as tk
from tkinter import filedialog
from core import StringGenerator,writefile
from visual.appconfig import AppConfig
from tkinter import messagebox
from threading import Thread

class MainWindow(tk.Tk):

    _writing = False
    
    def __init__(self,config:AppConfig,*args,**kwargs):
        super().__init__(*args,**kwargs)
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
            messagebox.showerror('Invalid arguments','<Min chars count> must be less or equal to <Max chars count>')
            pass
        else:
            self._generator.min_length = self._min_chars_count.get()
            self._generator.max_length = self._max_chars_count.get()        
            with filedialog.askopenfile(mode='w') as file:
                Thread(daemon=True,target=lambda:self._write_strings(file.name)).start()   
                pass
            pass
        pass

    def _validate_params(self):
        return self._min_chars_count.get() <= self._max_chars_count.get()

    def _write_strings(self,file:str):
        self._writing = True
        text = ''
        for string in self._generator.GenerateStrings(self._lines_count.get()):
            text += string + '\n'
            pass
        text = text[:len(text) - 1]
        writefile(file,text)
        self._writing = False
        pass

    def _on_close(self):
        if self._writing:
            if messagebox.askyesno('Salir','Desea detener el proceso de escritura?'):
                self.destroy()
                pass
            pass
        else:
            self.destroy()
            pass
        pass

    pass