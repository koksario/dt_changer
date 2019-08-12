import filecmp
import os


my_path = "d:\\"
a = os.listdir(path=os.path.abspath(my_path))
dir1 = a[1]
dir2 = a[2]
print(dir1, dir2)
x = filecmp.dircmp(dir1, dir2)
