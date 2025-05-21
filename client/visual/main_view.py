import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from visual.appconfig import AppConfig
from tkinter import messagebox
import sys
import os
import platform
import signal
from core import removefile,StringGenerator
from multiprocessing import Value,Process,Lock,cpu_count,Array
import time
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from protocol import ServerOperation,Request,Response,Status
from tools import sendto

class MainWindow(tk.Tk):

    _progress_bar = None
    _writing = Value('i',0)
    _file = ''
    _cpus = cpu_count()
    _lock = Lock()
    _generator = None
    _process = None
    _process_in_course = None
    _progress = Value('i',0)

    def __init__(self,config:AppConfig,*args,**kwargs):
        self._config = config
        super().__init__(*args,**kwargs)
        self._pattern = config.pattern
        if 'size' in config.interface.keys():
            self.geometry(f'{config.interface["size"]}')
            pass

        if 'window' in config.interface.keys():
            self.configure(**config.interface['window'])
            pass

        self.title('Vista Principal')
        self.protocol('WM_DELETE_WINDOW',lambda:self._on_close())
        
        # container for the params controls
        self._params_box = tk.Frame(self)
        in_bg = None
        in_fg = None
        if 'input_bg' in config.interface.keys():
            in_bg = config.interface['input_bg']
            pass
        if 'input_fg' in config.interface.keys():
            in_fg = config.interface['input_fg']
            pass
        if 'input_controls' in config.interface.keys():
            self._params_box.configure(**config.interface['input_controls'])
            pass
        self._params_box.pack(side=tk.TOP,pady=50)

        # container for the count of lines to write in the file
        self._string_lines_count_input_box = tk.Frame(self._params_box)
        if 'input_controls' in config.interface.keys():
            self._string_lines_count_input_box.configure(**config.interface['input_controls'])
            pass
        self._string_lines_count_input_box.pack(side=tk.LEFT,padx=30)

        # lines
        self._lines_count = tk.IntVar(self._string_lines_count_input_box)
        self._lines_count.set(1000000)
        self._string_input_label = tk.Label(self._string_lines_count_input_box,text='Cantidad de cadenas')
        if 'input_controls' in config.interface.keys():
            self._string_input_label.configure(**config.interface['input_controls'])
            pass
        self._string_input_label.pack(side=tk.TOP)
        self._string_count_input = tk.Spinbox(
            self._string_lines_count_input_box,
            from_=config.min_lines if config.min_lines != None else 10,
            to=config.max_lines if config.max_lines != None else 2000000,
            increment=config.lines_increment if config.lines_increment != None else 1000,
            textvariable=self._lines_count,
            bg=in_bg if in_bg != None else self.cget('bg'),
            fg=in_fg if in_fg != None else self.cget('fg')
        )
        self._string_count_input.pack(side=tk.BOTTOM)

        # container for the min count of characters
        self._min_chars_count_input_box = tk.Frame(self._params_box)
        if 'input_controls' in config.interface.keys():
            self._min_chars_count_input_box.configure(**config.interface['input_controls'])
            pass
        self._min_chars_count_input_box.pack(side=tk.LEFT,padx=30)

        # min count characters
        self._min_chars_count = tk.IntVar(self._min_chars_count_input_box)
        self._min_chars_count.set(config.min_chars)
        self._min_char_count_label = tk.Label(self._min_chars_count_input_box,text='Min. caracteres')
        if 'input_controls' in config.interface.keys():
            self._min_char_count_label.configure(**config.interface['input_controls'])
            pass
        self._min_char_count_label.pack(side=tk.TOP)
        self._min_chars_count_input = tk.Spinbox(
            self._min_chars_count_input_box,
            from_=config.min_chars,
            to=config.max_chars,
            increment=config.chars_increment if config.chars_increment != None else 10,
            textvariable=self._min_chars_count,
            bg=in_bg if in_bg != None else self.cget('bg'),
            fg=in_fg if in_fg != None else self.cget('fg')
        )
        self._min_chars_count_input.pack(side=tk.BOTTOM)

        # container for the max count of characters
        self._max_chars_count_input_box = tk.Frame(self._params_box)
        if 'input_controls' in config.interface.keys():
            self._max_chars_count_input_box.configure(**config.interface['input_controls'])
            pass
        self._max_chars_count_input_box.pack(side=tk.LEFT,padx=30)

        # max count characters
        self._max_chars_count = tk.IntVar(self._max_chars_count_input_box)
        self._max_chars_count.set(config.max_chars)
        self._max_chars_count_label = tk.Label(self._max_chars_count_input_box,text='Max. caracteres')
        if 'input_controls' in config.interface.keys():
            self._max_chars_count_label.configure(**config.interface['input_controls'])
            pass
        self._max_chars_count_label.pack(side=tk.TOP)
        self._max_chars_count_input = tk.Spinbox(
            self._max_chars_count_input_box,
            from_=config.min_chars,
            to=config.max_chars,
            increment=config.chars_increment if config.chars_increment != None else 10,
            textvariable=self._max_chars_count,
            bg=in_bg if in_bg != None else self.cget('bg'),
            fg=in_fg if in_fg != None else self.cget('fg')
        )
        self._max_chars_count_input.pack(side=tk.BOTTOM,padx=30)

        # container for the cpus to use
        self._cpus_count_input_box = tk.Frame(self._params_box)
        if 'input_controls' in config.interface.keys():
            self._cpus_count_input_box.configure(**config.interface['input_controls'])
            pass
        self._cpus_count_input_box.pack(side=tk.LEFT,padx=30)

        # cpu input
        self._cpu_count = tk.IntVar(self._cpus_count_input_box)
        self._cpu_count.set(config.cpu if config.cpu != None else 1)
        self._cpu_count_label = tk.Label(self._cpus_count_input_box,text='Procesos por nucleo')
        if 'input_controls' in config.interface.keys():
            self._cpu_count_label.configure(**config.interface['input_controls'])
            pass
        self._cpu_count_label.pack(side=tk.TOP)
        self._cpu_count_input = tk.Spinbox(
            self._cpus_count_input_box,
            from_=1,
            to=config.max_cpu if config.max_cpu != None else 5,
            increment=1,
            textvariable=self._cpu_count,
            bg=in_bg if in_bg != None else self.cget('bg'),
            fg=in_fg if in_fg != None else self.cget('fg')
        )
        self._cpu_count_input.pack(side=tk.BOTTOM,padx=30)

        # controls for the app
        self._buttons_box = tk.Frame(self)
        if 'buttons_controls' in config.interface.keys() and 'container' in config.interface['buttons_controls'].keys():
            self._buttons_box.configure(**config.interface['buttons_controls']['container'])
            pass
        self._buttons_box.pack(side=tk.BOTTOM,pady=50)

        self._file_generator_btn = tk.Button(self._buttons_box,text='Generar fichero',command=lambda:self._save_file())
        self._stop_generation_btn = tk.Button(self._buttons_box,text='Detener generacion',command=lambda:self._stop_file_generation())
        self._send_file_btn = tk.Button(self._buttons_box,text='Enviar fichero',command=lambda:self._send_file())

        if 'buttons_controls' in config.interface.keys() and 'buttons' in config.interface['buttons_controls'].keys():
            self._file_generator_btn.configure(**config.interface['buttons_controls']['buttons'])
            self._stop_generation_btn.configure(**config.interface['buttons_controls']['buttons'])
            self._send_file_btn.configure(**config.interface['buttons_controls']['buttons'])
            pass

        self._file_generator_btn.pack(side=tk.LEFT,pady=10,padx=10)
        self._stop_generation_btn.pack(side=tk.LEFT,padx=10,pady=10)
        self._send_file_btn.pack(side=tk.LEFT,padx=10,pady=10)
        
        self.mainloop()

        pass

    def _send_file(self):
        file = filedialog.askopenfilename()
        request = Request(Operation=ServerOperation.START_FILE_PONDERATION)
        response = sendto(self._config.host,self._config.port,request)
        if response.Status != Status.OK:
            messagebox.showerror('Server error',response.StatusMessage)
            return
        request = Request(Operation=ServerOperation.SEND_FILE)
        with open(file,'r') as reader:
            words = [word for word in map(lambda string:string.replace('\n',''),reader.readlines()) if len(word) > 0]
            request.Body = {'words':words}
            response = sendto(self._config.host,self._config.port,request)
            pass
        request = Request(Operation=ServerOperation.PONDERATION)
        request.Body = {
            'process_by_cpu':self._cpu_count.get(),
            'strings_by_process':self._config.max_strings_by_process
        }
        response = sendto(self._config.host,self._config.port,request)
        dot_extension = file.rindex('.')
        with open(f'{file[:dot_extension]}_result.txt','w') as writer:
            for r in response.Body['results']:
                writer.write(f'{r}\n')
                pass
            pass
        request = Request(Operation=ServerOperation.END_FILE_PONDERATION)
        response = sendto(self._config.host,self._config.port,request)
        if response.Status != Status.OK:
            messagebox.showerror('Server error',response.StatusMessage)
            pass
        else:
            messagebox.showinfo('Operation done',f'Analisis completado en {response.Body["time"]}')
            pass
        pass

    def _check_writing_process(self):
        # checks for the end of the writing process and update the progresbarr status
        if self._writing.value == 1:
            self._progress_bar['value'] = self._progress.value
            self.after(1,lambda:self._check_writing_process())
            pass
        else:
            if self._process != None:
                self._process.join()
                self._process = None
                pass
            if self._progress_bar != None:
                self._progress_bar.destroy()
                self._progress_bar = None
                pass
            pass
        pass

    def _save_file(self):
        if not self._validate_params():
            messagebox.showerror('Invalid arguments','<Min chars count> must be less than <Max chars count>')
            pass
        else:
            self._progress.value = 0
            self._file = filedialog.asksaveasfilename()
            self._progress_bar = ttk.Progressbar(
                self,
                orient=tk.HORIZONTAL,
                mode='determinate',
                length=300,
                maximum=self._lines_count.get()
            )
            self._writing.value = 1
            self._progress_bar.pack(side=tk.TOP)
            # to keep safe the multiprocessing process
            if __name__ == '__mp_main__':
                return
            # create the stack of process in course
            with self._lock:
                self._process_in_course = Array('i',self._cpus*self._cpu_count.get())
                pass
            # spawn the writing process
            self._process = Process(target=lambda:self._start_writing(),name='writing_process')
            self._process.start()
            # checks for the end of the writing process
            self.after(1,lambda:self._check_writing_process())
            pass
        pass

    def _start_writing(self):
        # starts the writing process in the file

        # limit of strings by cpu
        lines_by_process = self._config.max_strings_by_process
        # total of strings to write
        total = self._lines_count.get()
        # if there is less than 'lines_by_process' strings to write
        if total < lines_by_process:
            # share the task bettwen all the cpu
            lines_by_process = total // (self._cpu_count.get()*self._cpus)
            pass
        # calculate the amount of process needed to write all the strings
        processes_needed = total // lines_by_process
        # adds one more process if needed
        if processes_needed*lines_by_process < total:
            processes_needed += 1
            pass
        # create the string generator
        self._generator = StringGenerator(
            pattern=self._pattern,
            min_length=self._min_chars_count.get(),
            max_length=self._max_chars_count.get()
        )
        # to keep safe the multiprocessing process
        if __name__ == '__mp_main__':
            return
        # while there are process to do
        while processes_needed > 0:
            # process stack
            processes = []
            for i in range(min(self._cpus*self._cpu_count.get(),processes_needed)):
                # total of strings for this process
                p_total = lines_by_process if total > lines_by_process else total
                p = Process(target=lambda:self._write_strings(p_total),name=f'p{i}')
                # update the total
                total -= p_total
                processes_needed -= 1
                # spawn the process
                p.start()
                processes.append(p)
                pass
            # acquire the control over the stack of process in course
            with self._lock:
                # updates the pids of the process in course
                for i in range(len(processes)):
                    self._process_in_course[i] = processes[i].pid
                    pass
                pass
            # wait for the end of the process
            for p in processes:
                if p != None:
                    p.join()
                pass
            with self._lock:
                for i in range(len(processes)):
                    self._process_in_course[i] = 0
                    pass
                pass
            pass
        with self._lock:
            if self._process_in_course != None:
                self._process_in_course = None
                pass
            pass
        text = ''
        with open(self._file,'r') as reader:
            text = reader.read()
            pass
        if text.endswith('\n'):
            with open(self._file,'w') as writer:
                writer.write(text[:len(text) - 1])
                pass
            pass
        self._writing.value = 0
        pass

    def _write_strings(self,count:int):
        text = ''
        for word in self._generator.GenerateStrings(count):
            text += f'{word}\n'
            self._progress.value += 1
            pass
        with self._lock:
            # adds the new strings to the file
            with open(self._file,'a') as writer:
                writer.write(text)
                pass
            pass
        pass

    def _validate_params(self):
        return self._min_chars_count.get() < self._max_chars_count.get()

    def _stop_process_in_course(self):
        # stop all the writing process
        self._process.kill()
        if self._process != None:
            self._process = None
        with self._lock:
            # stop the subprocess
            if self._process_in_course != None:
                for process in self._process_in_course:
                    if process > 0:
                        os.kill(process,signal.SIGTERM)
                        pass
                    pass
                self._process_in_course = None
                pass
            pass
        # remove the file if exists
        if os.path.exists(self._file):
            removefile(self._file)
            pass
        self._file = ''
        pass

    def _stop_file_generation(self):
        if self._writing.value == 1:
            if messagebox.askyesno('Writing in process','There is a process in progress'):
                self._stop_process_in_course()
                pass
            self._writing.value = 0
            pass
        pass

    def _on_close(self):
        if self._writing.value == 1:
            if messagebox.askyesno('Writing in process','There is a process in progress'):
                self._stop_process_in_course()
                pass
            self._writing.value = 0
            pass
        else:
            self.destroy()
            pass
        pass

    def _get_color_from_text(self,text:str):
        if text.lower().startswith('rgb'):
            r,g,b = re.findall('\d+',text)
            return self._rgb_to_hex(int(r),int(g),int(b))
        return text

    def _rgb_to_hex(self,r:int,g:int,b:int):
        exception_msg = 'the values most be in range 0-255'
        if r < 0 or r > 255:
            raise ValueError(exception_msg)
        if g < 0 or g > 255:
            raise ValueError(exception_msg)
        if b < 0 or b > 255:
            raise ValueError(exception_msg)
        return f'#{r:02x}{g:02x}{b:02x}'

    pass