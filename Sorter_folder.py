import os
import shutil
from zipfile import ZipFile
import concurrent.futures
from time import time
import logging


path = 'D:/Мотлох/'
list_ = os.listdir(path)
slovn = {'video': ['AVI', 'MP4', 'MOV', 'MKV'],
         'images': ['JPEG', 'PNG', 'JPG', 'SVG', 'BMP'],
         'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
         'audio': ['MP3', 'OGG', 'WAV', 'AMR'],
         'archives': ['ZIP', 'GZ', 'TAR'], }



def move(type,re_name_path,re_name):
    if os.path.exists(path+'/'+type):
        shutil.move(re_name_path, path+'/'+type+'/'+re_name)
    else:
        os.makedirs(path+'/'+type)
        shutil.move(re_name_path, path+'/'+type+'/'+re_name)



def zip_unpack(re_name_path,name):
    if os.path.exists(path+'/'+'archives'):

        path_zip = os.path.join(path+'/'+'archives', name)
        os.mkdir(path_zip)
        with ZipFile(re_name_path, 'r') as zip_file:
            zip_file.extractall(
                path=path+'/'+'archives'+'/'+name)
            os.remove(re_name_path)
    else:
        os.makedirs(path+'/'+'archives')
        with ZipFile(re_name_path, 'r') as zip_file:
            zip_file.extractall(
                path=path+'/'+'archives'+'/'+name)

        os.remove(re_name_path)


def normalize(name):
    Ukr = "абвгдежзийклмнопрстуфхцчшщъыьэюяєіїґ"
    Eng = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
           "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    TRANS = {}
    for c, l in zip(Ukr, Eng):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()
    return name.translate(TRANS)




def sort(file_):
            logging.debug(file_)
            name, ext = os.path.splitext(file_)
            print(name)
            file_ = os.path.join(path, file_)
            ext = ext[1:]
            if ext == '':
                if name != 'images' or name != 'documents' or name != 'audio' or name != 'video' or name != 'archives':
                    if not os.listdir(file_):
                            os.rmdir(file_)
            else:
                    re_name = normalize(name)+'.'+ext
                    re_name_path = path+re_name
                    os.rename(file_, re_name_path)
                    for k, v in slovn.items():
                        if ext.upper() in v:
                            try:
                                if k != 'archives':
                                    move(k,re_name_path,re_name)
                                else:
                                    zip_unpack(re_name_path,name)
                            except FileNotFoundError:
                                continue
                        else:
                            continue



timer = time()
logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(sort, list_)


logging.debug(f'{time()-timer}')