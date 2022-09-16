from ftplib import FTP
import os

ftp = FTP(host="files.000webhost.com", user="diiafake",passwd="qwer232309")
ftp.cwd('public_html/v')
ftp.retrlines('LIST')

def ftp_upload(filename, file, ftype='TXT'):
    """
    Функция для загрузки файлов на FTP-сервер
    @param ftp_obj: Объект протокола передачи файлов
    @param path: Путь к файлу для загрузки
    """
    ftp.cwd('photo')
    if ftype == 'TXT':
            ftp.storlines('STOR ' + f"{filename}", file)
    else:
            ftp.storbinary('STOR ' + f"{filename}", file, 1024)
    ftp.cwd("./")

def ftp_upload_with(filename, path, ftype='TXT'):
    """
    Функция для загрузки файлов на FTP-сервер
    @param ftp_obj: Объект протокола передачи файлов
    @param path: Путь к файлу для загрузки
    """
    ftp.cwd('photo')
    if ftype == 'TXT':
        with open(path) as fobj:
            ftp.storlines('STOR ' + f"{filename}", fobj)
    else:
        with open(path, 'rb') as fobj:
            ftp.storbinary('STOR ' + f"{filename}", fobj, 1024)
    ftp.cwd("./")