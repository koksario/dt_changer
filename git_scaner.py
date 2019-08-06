import os

#
# my_path = input("Абсолютный путь к папке с файлами (вида C:\\dir) > ")
my_path = "d:\\git\\gg\\dt_changer"
time_dic = {}


def list_create():
    a = os.listdir(path=os.path.abspath(my_path))
    for i in a:
        x = os.path.getmtime(i)
        # На этом этапе у нас есть:
        # 'a' - список файлов в папке по алфавиту
        # 'i' - отдельный очередной файл
        # 'x' - его 'контрольное число'(время изменения в миллисекундах)
        # 'time_dic' - (в самом начале пустой)
        #                           словарь вида "имя файла"=контрольное_число
        if i in time_dic.keys():
            if time_dic[i] != x:
                print(i + " изменён!\n" + str(time_dic[i]) + "vs\n" + str(x))
                time_dic[i] = x
            else:
                pass
        else:
            time_dic[i] = x



while True:
    list_create()
