import sys
import subprocess
import os
from datetime import datetime
from pathlib import Path


# def vali_dir(code):
#     """Приём пути и проверка его на правильность"""
#     my_var = {
#         'conf': 'Абсолютный путь к папке с конфигами (вида C:\\dir) > ',
#         'job': 'Абсолютный путь к месту с файлом-списком (вида C:\\dir) > ',
#         'cli': 'Абсолютный путь к месту с jenkins-cli.jar (вида C:\\dir) > '}
#     while True:
#         req_path = input(
#             my_var[code])
#         if req_path == 'q' or req_path == 'Q':
#             sys.exit()
#         req_path = Path(req_path)
#         try:
#             tmp = req_path.is_dir()
#         except OSError:
#             print("Неправильный путь или нет такой папки")
#         else:
#             if not tmp:
#                 print("Неправильный путь или нет такой папки")
#                 continue
#             else:
#                 return req_path
#                 break


def list_name():
    """Приём названия списка и создание питон-списка из файла-списка"""
    global lname
    while True:
        lname = input("Полное имя файла-списка (вида list.txt) > ")
        lpath = job_path + "\\" + lname
        lpath = Path(lpath)
        if lname == 'q' or lname == 'Q':
            sys.exit()
        try:
            tmp = lpath.is_file()
        except OSError:
            print("Неправильное имя файла")
        else:
            if not tmp:
                print("Неправильное имя файла")
                continue
            else:
                # utf-8 - это, для корректного чтения, а sig для избежания
                # некого \ufeff (гугл в помощь)
                with open(lpath, encoding="utf-8-sig") as x:
                    job_list = x.read().splitlines()
                    print(job_list)
                return job_list
                break


def dir_maker():
    with open('create_dir.bat', 'w', encoding='utf-8') as x:
        scr_text = "@echo off\n" + "chcp 65001 >nul\n" + \
                   "@<\"" + lname + "\" " + \
                   "(for /f \"delims=\" %%i in (\'more\') " + \
                   "do md \".\\job_dir\\%%~i\")"
        x.write(scr_text)
    abs_bat = os.path.abspath('.\\create_dir.bat')
    subprocess.call([abs_bat])


def conf_copier():
    with open('copy_file.bat', 'w', encoding='utf-8') as x:
        scr_text = "@echo off\n" + "chcp 65001 >nul\n" + \
                   "@<\"" + lname + "\" " + \
                   "(for /f \"delims=\" %%i in (\'more\') do (\n" + \
                   "\tcopy \"\\\\192.168.1.100\\c$\\Program " + \
                   "Files\\Super_dir\\Jenkins\\jobs\\%%~i\\*.xml\" " + \
                   "\".\\job_dir\\%%~i\\*.xml\"\n" + "\t)\n)"
        x.write(scr_text)
    abs_bat = os.path.abspath('.\\copy_file.bat')
    subprocess.call([abs_bat])


def job_maker(j_l, cli_path, conf_path):
    """Создаватель(есть такое слово?) job'ов"""
    for i in j_l:
        jm = "cmd /c \'java -jar " + "\"" + cli_path + \
             "\\jenkins-cli.jar\" -auth your_jen_login:" + \
             "your_jen_token -s " + \
             "http://jenkins_server create-job " + "\"" + \
             str(i) + "\" < " + "\"" + conf_path + "\\" + str(i) + \
             "\\config.xml\"\'"
        # Выполнение команд в PowerShell
        subprocess.Popen(['powershell', jm]).wait(timeout=None)
        print()


# Основной ход программы
print("Для выхода введите 'q'", end='\n\n')
conf_path = str(os.path.abspath('.\\job_dir'))
# job_path = str(vali_dir('job'))
# cli_path = str(vali_dir('cli'))
job_path = str(os.path.abspath('.'))
cli_path = str(os.path.abspath('.'))
j_l = list_name()
# Создание папок
dir_maker()
conf_copier()
# Создание джобов
job_maker(j_l, cli_path, conf_path)
subprocess.Popen(['powershell', "pause"]).wait(timeout=None)
