@echo off
cmd /k "cd /d C:\Users\datas\PycharmProjects\main\D1\msfs-programs\ms-env\Scripts & activate & cd /d C:\Users\datas\PycharmProjects\main\D1\msfs-programs & python fscom.py %1 & TIMEOUT /T 3 /NOBREAK & exit"
