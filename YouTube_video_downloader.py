from moviepy.editor import VideoFileClip, AudioFileClip
from pytube.pytube import YouTube 
import os
import shutil
import logging


def on_progress(video_stream,total_size, bytes_remaining):
    total_size = video_stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent = (bytes_downloaded / total_size) * 100
    print("\r" + "▌" * int(percent) + " " * (100 - int(percent)) + " {}%".format(int(percent)), end='')

def on_finish(video_stream,total_size):
    file_title = f"{video_stream.title} {'audio' if video_stream.includes_audio_track else 'video'}"
    logging.warning(f"\nPobrano pliku {file_title} {'\n' if file_title.endswith('video') else ''}")

def Download():
    Czy_Tak = str(input("Czy chcesz pobierać pliki masowo? [Tak/Nie]: "))
    out = str(input(r"Ścieżka pod którą ma być zapisany plik: "))

    if Czy_Tak.lower() == 'tak':
        file = str(input(r'Podaj ścieżkę pliku z listą filmów do pobrania [musi to być plik TXT z oddzielonym każdym linkiem przecinkiem]: '))
        with open(file, 'r+') as f:
            temp_dir = create_temp_dir()

            for line in f:
                line.splitlines(keepends=True)
                videos = line.split(sep=',')

                print(line, sep=',', end='\n')

                for video in videos:
                    video = video.strip()
                    try:
                        youtubeObject = YouTube(video, 
                                                on_progress_callback=on_progress,
                                                on_complete_callback=on_finish, 
                                                use_oauth=True, 
                                                allow_oauth_cache=True,)
                        youtubeObject_audio, youtubeObject_video = get_video_audio(youtubeObject)
                        video_path, audio_path = download_video_audio(temp_dir, 
                                                                    youtubeObject_audio, 
                                                                    youtubeObject_video,)
                        merged_file_path = create_merged_file_dir(basedir= out, file= video_path)
                        combine_video_audio(vidname= video_path, 
                                            audname= audio_path, 
                                            outname= merged_file_path, 
                                            fps=30,)
                        
                        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

                    except Exception as e:
                        print("An error has occurred", e, end="\n\n")
                    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

            remove_temp_dir(temp_dir)

    elif Czy_Tak.lower() == 'nie':
        http = str(input(r'Podaj ścieżkę pliku do pobrania z linkiem HTTPs: '))

        youtubeObject = YouTube(http, on_progress_callback=on_progress,on_complete_callback=on_finish, use_oauth=True, allow_oauth_cache=True)
        youtubeObject_audio, youtubeObject_video = get_video_audio(youtubeObject)
        logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.warning('Pobieranie pliku')

        try:
            temp_dir = create_temp_dir()
            video_path, audio_path = download_video_audio(temp_dir, youtubeObject_audio, youtubeObject_video)
            merged_file_path = create_merged_file_dir(basedir= out, file= video_path)
            combine_video_audio(vidname= video_path, 
                                audname= audio_path, 
                                outname= merged_file_path, 
                                fps=youtubeObject_video.fps,)
            remove_temp_dir(temp_dir)

        except Exception as e:
            print("\n\nAn error has occurred: ",e)

    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def create_temp_dir():
    get_cwd = os.getcwd()
    temp_dir = os.path.join(get_cwd,'.hidden')

    if os.path.exists(temp_dir):
        remove_temp_dir(temp_dir)

    os.mkdir(temp_dir)
    os.popen(f"attrib +h {temp_dir}")

    return temp_dir

def remove_temp_dir(temp_dir):
    shutil.rmtree(temp_dir)

def get_video_audio(youtubeObject):
    youtubeObject = youtubeObject.streams
    youtubeObject_audio = youtubeObject.filter(only_audio=True).first()
    youtubeObject_video = youtubeObject.filter(file_extension="mp4").order_by('resolution').desc().first()

    return youtubeObject_audio, youtubeObject_video

def download_video_audio(temp_dir, youtubeObject_audio, youtubeObject_video):
    youtubeObject_audio.download(temp_dir,filename_prefix="audio ")
    youtubeObject_video.download(temp_dir,filename_prefix="video ")

    filename = youtubeObject_video.default_filename
    
    video_path = os.path.join(temp_dir, f"video {filename}")
    audio_path = os.path.join(temp_dir, f"audio {filename}")

    return video_path, audio_path

def create_merged_file_dir(basedir, file):
    name_file = os.path.basename(file).replace("video ","")
    path = os.path.join(basedir,name_file)

    return path

def combine_video_audio(vidname, audname, outname, fps=30):
    my_clip = VideoFileClip(vidname)
    audio_background = AudioFileClip(audname)
    final_clip = my_clip.set_audio(audio_background)
    final_clip.write_videofile(outname,fps=fps)

if __name__ == "__main__":
    Download()