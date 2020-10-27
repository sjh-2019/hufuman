import tkinter as tk
import tkinter.filedialog
from tkinter.filedialog import askdirectory
from hufuman import compress,decompress
top=tk.Tk()
top.title("解压缩")
top.geometry('500x300')
input_f=''
output_f=''
def selectPath():
    global input_f
    input_f = tk.filedialog.askopenfilename()

def selectPath1():
    global output_f
    output_f = askdirectory()+'output.txt'
tk.Button(top, text = "输入文件", command = selectPath).pack()
tk.Button(top, text = "输入文件路径", command = selectPath1).pack()


on_com=False
var=tk.StringVar()
l = tk.Label(top, textvariable=var, bg='white', fg='black', font=('Arial', 12), width=30, height=2)
def com_me():#压缩按钮函数
    compress(input_f,output_f)
    var.set('压缩成功')

on_decom=False
def decom_me():#压缩按钮函数
    global on_decom
    if on_decom==False:
        on_decom=True
        decompress(input_f,output_f)
        var.set('解压成功')

b1 = tk.Button(top, text='compress', font=('Arial', 12), width=10, height=1, command=com_me)
b2 = tk.Button(top, text='hit me', font=('Arial', 12), width=10, height=1, command=decom_me)
b1.pack()
b2.pack()
l.pack()

top.mainloop()