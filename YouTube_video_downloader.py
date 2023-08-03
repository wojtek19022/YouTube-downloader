import os
from pytube import YouTube
import logging

def Download():

    Czy_Tak = str(input("Czy chcesz pobierać pliki masowo? [Tak/Nie]: "))
    out = str(input(r"Ścieżka pod którą ma być zapisany plik: "))

    if Czy_Tak.lower() == 'tak':
        file = str(input(r'Podaj ścieżkę pliku z listą filmów do pobrania [musi to być plik TXT z oddzielonym każdym linkiem przecinkiem]: '))
        with open(file, 'r+') as f:
            for i in f:
                i.splitlines(keepends=True)
                x = i.split(sep=',')

                print(x, sep=',', end='\n')

                for i in x:
                    youtubeObject = YouTube(i)
                    youtubeObject = youtubeObject.streams.get_highest_resolution()
                    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
                    logging.warning('Pobieranie pliku')
                    try:
                        youtubeObject.download(out)

                        os.getpid()

                    except:
                        print("An error has occurred")
                    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
                    logging.warning(f"Plik {i} zapisany")

    elif Czy_Tak.lower() == 'nie':
        http = str(input(r'Podaj ścieżkę pliku do pobrania z linkiem HTTPs: '))

        youtubeObject = YouTube(http)
        youtubeObject = youtubeObject.streams.get_highest_resolution()
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.warning('Pobieranie pliku')


    try:
        youtubeObject.download(out)
        os.getpid()

    except:
        print("An error has occurred")
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.warning('Plik zapisany')

Download()