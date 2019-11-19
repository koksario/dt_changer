#!/bin/bash
<< ///

Простой мониторинг выполнения последовательных связанных запросов

///

# параметры our_login и our_pass должны быть заполнены
our_login=""
our_pass=""
					 
sleep_time=5
# Основной цикл программы
while true
do
	# Получаем сессию;
	# Извлекается значение из полученных результатов и сохраняется в переменную
	# на полученной странице будет, к примеру, '..."session":"QWERTY123"}'
	# нас интересует "QWERTY123", извлекаем
	session=$(curl -s -d "login=$our_login&password=$our_pass" \
                         "http://192.168.1.100/request" \
                         | sed -n 's/.*session\":\"\([^\"]*\)\".*/\1/p')
						 # ещё вариант извлечения значения:
                         # | grep -o -P '(?<=session\":\").*(?=\"})')
	echo session=$session
	# На данном этапе происходит случайный выбор значений 
	# из таблицы, содержащей 4 столбца, разделённых табуляцией
	random_string=$(shuf -n 1 ~/super_table)
	param_1=$(echo "$random_string" | awk -F "\t" '{print $1}')
	param_2=$(echo "$random_string" | awk -F "\t" '{print $2}')
	param_3=$(echo "$random_string" | awk -F "\t" '{print $3}')
	param_4=$(echo "$random_string" | awk -F "\t" '{print $4}')

	if [ -n "$session" ]; then
		echo start tx_2
		param_5=$(curl -s -X POST "http://192.168.1.100/request&session=$session" | sed -n 's/.*param_5\":\([^}]*\)}.*/\1/p')
		
		if [ -n "$param_5" ]; then
			echo start tx_3
			# тело, указанное ниже, не обязательно экранировать; можно всё, 
			# кроме подставляемых параметров, заключить в одинарные кавычки
			# например, 
			# url='super"puper"request:"param_2"='$param_2'&session='$session
			url="super\"puper\"request:\"param_2\"=$param_2&session=$session"
			curl -d "$url" \
					'http://192.168.1.100/request' && echo -e "\n"

			echo start tx_4
			param_6=$(curl -s -X POST "http://192.168.1.100/request&param_5=$param_5&session=$session" | sed -n 's/.*param_6\":\([^,]*\),.*/\1/p')

			if [ -n "$param_6" ]; then
				echo start tx_5
				# сохраняем результат в файл, чтобы затем извлечь оттуда 
				# добрую часть параметров
				curl -s -o ~/super_output -X POST "http://192.168.1.100/request&param_1=$param_1&session=$session"
				param_8=$(sed -n 's/.*param_8\":\([0-9]*\),.*/\1/p' ~/super_output)
				param_7=$(sed -n 's/.*param_7\":\([0-9]*\),.*/\1/p' ~/super_output)
				if [[ $param_8 != 0 && $param_7 == 2 ]]; then
					echo start tx_6_1
					param_b=$(sed -n 's/.*param_b\":\"\([^\"]*\)\".*/\1/p' ~/super_output)
					param_9=$(sed -n 's/.*param_9\":\"\([^\"]*\)\".*/\1/p' ~/super_output)
					param_a=$(sed -n 's/.*param_a\":\"\([^\"]*\)\".*/\1/p' ~/super_output)
					echo param_a=$param_a
					url="param_2=$param_2&param_3=$param_3&param_6=$param_6&param_5=$param_5&param_4={\"param_b\": \"$param_b\",\"param_9\": \"$param_9\",\"param_a\": \"$param_a\"}&session=$session"
					curl -d "$url" \
					        'http://192.168.1.100/request' && echo -e "\n"
				else
					echo start tx_6_2
					url="param_2=$param_2&param_3=$param_3&param_6=$param_6&param_5=$param_5&session=$session"
					curl -d "$url" \
					        'http://192.168.1.100/request' && echo -e "\n"
				fi
				echo start tx_7
				url="param_5=$param_5&param_1=$param_1&param_4=$param_4&session=$session"
				curl -d "$url" \
					    'http://192.168.1.100/request' && echo -e "\n"
			fi
		fi
	fi

	sleep $sleep_time
done
