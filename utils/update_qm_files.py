import glob
import os
import subprocess

# Converts all .ts into .qm

def update_qm_files() -> None:
    files = glob.glob(os.path.join('.', 'translations', '*.ts'))
    trans_bi_dir = os.path.join('.', 'src', 'lang')

    for file_name in files:
        print('Converting ' + file_name)
        file_name_bi = file_name[:-2] + 'qm'
        subprocess.call(['pyside6-lrelease', file_name, '-qm', os.path.join(trans_bi_dir, file_name_bi)])
    
    print(os.listdir(trans_bi_dir))

update_qm_files()