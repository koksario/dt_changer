@echo off
REM скрипт для вывода количества time_wait на текущий момент
REM вывод каждые 2 секунды
REM нажатие ENTER в строке позволяет отображать результаты быстрее
:loop
set ttt=%TIME:~-11,8%
FOR /F "usebackq" %%a IN (`netstat -n -a ^| find /I /c "time_wait"`) DO (
 set nnn=%%a
)

echo [%ttt%]	%nnn%
timeout /t 2 > Nul
goto :loop
