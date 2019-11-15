"""
Быстрое копирование какого-то файла из разных папок
в другое место с идентичной структурой
В данном случае это build.xml
программа не рассчитана на файлы build.xml, спрятанные в подпапках"""
from shutil import copyfile
import os

# Создаём список папок, которые есть в \\jenkins_server\share_dir_work
dirlist = os.listdir("\\\\jenkins_server\\share_dir_work\\")
# Из каждой папки в списке копируем файл build.xml(если он есть) в 
# соответствующую директорию(рабочая папка git'а, в данном случае это с:\git\my_git_dir\)
for i in dirlist:
    try:
        copyfile("\\\\jenkins_server\\share_dir_work\\" + i + "\\build.xml", "d:\\git\\my_git_dir\\jenkins\\jobs\\" + i + "\\build.xml")
    except FileNotFoundError:
        print(i + " - это либо файл, либо директория без build.xml")