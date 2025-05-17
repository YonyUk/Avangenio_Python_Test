import tkinter as tk
from tkinter import filedialog

class MainWindow(tk.Tk):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.geometry('800x600')
        self.title('MainView')
        self._file_generator_btn = tk.Button(self,text='generate random file',command=lambda:self._save_file())
        self._file_generator_btn.pack(side=tk.BOTTOM,pady=10)

        self.mainloop()

        pass

    def _save_file(self,path=''):
        with filedialog.asksaveasfile(mode='w') as writer:
            
            pass
        pass

    pass