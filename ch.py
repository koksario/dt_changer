import sys
import subprocess
from datetime import datetime
from pathlib import Path

def vali_dir():
    """Приём пути и проверка его на правильность"""
    global dir_ectory
    while True:
        dir_ectory = input(
            "Абсолютный путь к папке с файлами (вида C:\\dir) > ")
        if dir_ectory == 'q' or dir_ectory == 'Q':
            sys.exit()
        dir_ectory = Path(dir_ectory)
        try:
            tmp = dir_ectory.is_dir()
        except OSError:
            print("Неправильный путь или нет такой папки")
        else:
            if not tmp:
                print("Неправильный путь или нет такой папки")
                continue
            else:
                break

def vali_date(code):
    """Приём даты/времени и проверка на валидность"""
    d_o_t_dic = {
        'for_time': ['Время создания и изменения (вида 12:00:00) > ', '%H:%M:%S',
               '(ЧЧ:ММ:СС или Ч:М:С)'],
        'for_date': ['Дата создания и изменения (вида 01/01/2001) > ', '%d/%m/%Y',
               '(ДД/ММ/ГГГГ или Д/М/ГГГГ)']}
    while True:
        d_or_t = input(
            d_o_t_dic[code][0])
        if d_or_t == 'q' or d_or_t == 'Q':
            sys.exit()
        try:
            # Проверяем, что дата введена в нужном формате
            datetime.strptime(d_or_t, d_o_t_dic[code][1])
        except ValueError:
            print(d_o_t_dic[code][2])
        else:
            return d_or_t

def formate_date():
    """Обработка даты из вида МЕСЯЦ/день/год в вид ДЕНЬ/МЕСЯЦ/год"""
    global date_of_change
    tmp = datetime.strptime(date_of_change, "%d/%m/%Y")
    date_of_change = tmp.strftime('%m/%d/%Y')

def changer(dir_ectory, date_of_change, time_of_change):
    """Генератор строк для PowerShell"""
    dir_ectory = str(dir_ectory)
    date_of_change = str(date_of_change)
    time_of_change = str(time_of_change)
    ch_cr = "Get-ChildItem  " + "\'" + dir_ectory + \
            "\\\'  -Recurse | % {$_.CreationTime = \'" + \
            date_of_change + " " + time_of_change + "\'}"
    ch_mod = "Get-ChildItem  " + "\'" + dir_ectory + \
             "\\\' -Recurse | % {$_.LastWriteTime = \'" + \
             date_of_change + " " + time_of_change + "\'}"
    global cr_and_mod
    cr_and_mod = ch_cr + "; " + ch_mod

while True:
    # Основной цикл программы
    print("Для выхода введите 'q'", end='\n\n')
    vali_dir()
    date_of_change = vali_date('for_date')
    formate_date()
    time_of_change = vali_date('for_time')

    # Создание строк для PowerShell
    changer(dir_ectory, date_of_change, time_of_change)

    # Выполнение команд в PowerShell
    proc = subprocess.Popen(['powershell', cr_and_mod]).wait(timeout=None)
    print()
