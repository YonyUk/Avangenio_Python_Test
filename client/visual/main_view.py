import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from visual.appconfig import AppConfig
from tkinter import messagebox
import sys
import subprocess
import os
import platform
import signal
from core import removefile

class MainWindow(tk.Tk):

    _progress_bar = None
    _subprocess = None
    _writing = False
    _file = ''

    def __init__(self,config:AppConfig,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self._pattern = config.pattern
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
        self._min_chars_count.set(config.min_chars)
        self._min_char_count_label = tk.Label(self._min_chars_count_input_box,text='Min count characters')
        self._min_char_count_label.pack(side=tk.TOP)
        self._min_chars_count_input = tk.Spinbox(
            self._min_chars_count_input_box,
            from_=config.min_chars,
            to=config.max_chars,
            increment=config.chars_increment if config.chars_increment != None else 10,
            textvariable=self._min_chars_count
        )
        self._min_chars_count_input.pack(side=tk.BOTTOM)

        # container for the max count of characters
        self._max_chars_count_input_box = tk.Frame(self._params_box)
        self._max_chars_count_input_box.pack(side=tk.LEFT,padx=30)

        # max count characters
        self._max_chars_count = tk.IntVar(self._max_chars_count_input_box)
        self._max_chars_count.set(config.max_chars)
        self._max_chars_count_label = tk.Label(self._max_chars_count_input_box,text='Max count characters')
        self._max_chars_count_label.pack(side=tk.TOP)
        self._max_chars_count_input = tk.Spinbox(
            self._max_chars_count_input_box,
            from_=config.min_chars,
            to=config.max_chars,
            increment=config.chars_increment if config.chars_increment != None else 10,
            textvariable=self._max_chars_count
        )
        self._max_chars_count_input.pack(side=tk.BOTTOM,padx=30)

        # container for the cpus to use
        self._cpus_count_input_box = tk.Frame(self._params_box)
        self._cpus_count_input_box.pack(side=tk.LEFT,padx=30)

        # cpu input
        self._cpu_count = tk.IntVar(self._cpus_count_input_box)
        self._cpu_count.set(config.cpu if config.cpu != None else 1)
        self._cpu_count_label = tk.Label(self._cpus_count_input_box,text='processes by cpu to use')
        self._cpu_count_label.pack(side=tk.TOP)
        self._cpu_count_input = tk.Spinbox(
            self._cpus_count_input_box,
            from_=1,
            to=config.max_cpu if config.max_cpu != None else 5,
            increment=1,
            textvariable=self._cpu_count
        )
        self._cpu_count_input.pack(side=tk.BOTTOM,padx=30)

        # controls for the app
        self._buttons_box = tk.Frame(self)
        self._buttons_box.pack(side=tk.BOTTOM,pady=50)

        self._file_generator_btn = tk.Button(self._buttons_box,text='generate random file',command=lambda:self._save_file())
        self._stop_generation_btn = tk.Button(self._buttons_box,text='Stop file generation',command=lambda:self._stop_writing(self._file))

        self._file_generator_btn.pack(side=tk.LEFT,pady=10,padx=10)
        self._stop_generation_btn.pack(side=tk.LEFT,padx=10,pady=10)

        self.mainloop()

        pass

    def _check_writing_process(self,file:str):
        if os.path.exists(f'{file}.lock') or self._subprocess != None:
            self.after(1,lambda:self._check_writing_process(file))
            pass
        else:
            self._writing = False
            pass
        pass

    def _save_file(self):
        if not self._validate_params():
            messagebox.showerror('Invalid arguments','<Min chars count> must be less than <Max chars count>')
            pass
        else:
            min_ = str(self._min_chars_count.get())
            max_ = str(self._max_chars_count.get())
            count = str(self._lines_count.get())
            cpu_count = str(self._cpu_count.get())
            file = filedialog.asksaveasfilename()
            self._file = file
            self._progress_bar = ttk.Progressbar(
                self,
                orient=tk.HORIZONTAL,
                mode='indeterminate',
                length=300
            )
            self._progress_bar.pack(side=tk.TOP)
            if sys.platform.startswith('win') or sys.platform.startswith('cygwin'):
                self._subprocess = subprocess.Popen(['python','writing_subrutine.py',file,self._pattern,min_,max_,count,cpu_count])
                pass
            elif sys.platform.startswith('linux'):
                self._subprocess = subprocess.Popen(['python3','writing_subrutine.py',file,self._pattern,min_,max_,count,cpu_count])
                pass
            else:
                pass
            self._writing = True
            self.after(1,lambda:self._check_writing_process(file))
            pass
        pass

    def _validate_params(self):
        return self._min_chars_count.get() < self._max_chars_count.get()

    def _stop_writing(self,file:str):
        if self._subprocess != None:
            for pid in get_children_pids(self._subprocess.pid):
                os.kill(pid,signal.SIGTERM)
                pass
            self._subprocess.kill()
            self._subprocess = None
            removefile(f'{file}.lock')
            if os.path.exists(file):
                removefile(file)
                pass
            pass
        if self._progress_bar != None:
            self._progress_bar.destroy()
            self._progress_bar = None
            pass
        pass

    def _on_close(self):
        if self._writing:
            if messagebox.askyesno('Salir','Desea detener el proceso de escritura?'):
                self._stop_writing(self._file)
                self._file = ''
                self.destroy()
                pass
            pass
        else:
            self.destroy()
            pass
        pass

    pass

def get_children_pids(pid:int):
    try:
        if  platform.system() == 'Windows':
            output = subprocess.check_output(
                f'wmic process where (ParentProcessId={pid}) get ProcessId',
                shell=True,
                stderr=subprocess.DEVNULL
            ).decode().strip()
            pids = [int(line) for line in output.split('\n')[1:] if line.strip()]
            return pids
        elif platform.system() == 'Linux':
            output = subprocess.check_output(
                [f'pgrep','-P',str(pid)],
                stderr=subprocess.DEVNULL
            ).decode().strip()
            return list(map(int,output.split())) if output else []
        else:
            return []
        pass
    except subprocess.CalledProcessError as ex:
        return []