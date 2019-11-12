"""программа не рассчитана на файлы build.xml, спрятанные в подпапках"""
from shutil import copyfile
import os

# Создаём список папок, которые есть в \\jenkins\work
dirlist = os.listdir("\\\\jenkins\\work\\")
# Из каждой папки в списке копируем файл build.xml(если он есть) в 
# соответствующую директорию(рабочая папка git'а, в данном случае это с:\git\tii-sys-eng\)
for i in dirlist:
    try:
        copyfile("\\\\jenkins\\work\\" + i + "\\build.xml", "d:\\git\\gg\\tii-sys-eng\\jenkins\\jobs\\" + i + "\\build.xml")
    except FileNotFoundError:
        print(i + " - это либо файл, либо директория без build.xml")