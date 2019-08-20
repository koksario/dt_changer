touch sysinfo_file_temp && touch tmp_script && tee -a tmp_script << EOF
#!/bin/bash

# Запись информации о ЦПУ во временный файл
cat /proc/cpuinfo > ~/sysinfo_file_temp

# Анализ информации и запись её в переменные с расчетом на возможный Hyper threading
number_cpu_raw=\$(cat sysinfo_file_temp | grep 'processor' | wc -l)
number_sibl=\$(cat sysinfo_file_temp | grep 'siblings' | egrep -o '([[:digit:]]+)' | uniq)
number_cpu_cores=\$(cat sysinfo_file_temp | grep 'cpu cores' | egrep -o '([[:digit:]]+)' | uniq)
coef=\$((number_sibl/number_cpu_cores))
number_cpu=\$((number_cpu_raw/coef))

# Удаление временного файла
rm -rf ~/sysinfo_file_temp

# Сбор ин-ции о памяти
memory=\$(cat /proc/meminfo | grep MemTotal | egrep -o '([[:digit:]]+)')
memory=\$((memory/1024))

# Хард
hdd=\$(df -P | egrep '^/dev/' | awk '{print \$2}' | awk '{s += \$1} END {print s}')
hdd=\$((hdd/1048576))

# ОС через костыль
clear
cat /etc/*-release
read -p "Введите информацию об ОС > " os

# Вывод информации
clear
echo "ЦП: \$number_cpu ЦП по \$number_cpu_cores ядра"
echo "ОЗУ: \$memory Мб"
echo "ЖД: ~\$hdd Гб"
echo "ОС: \$os"
EOF
chmod +x ./tmp_script && ./tmp_script && rm -rf ./tmp_script
