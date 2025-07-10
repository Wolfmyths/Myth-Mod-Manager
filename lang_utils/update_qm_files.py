import glob
import os
import subprocess

# Converts all .ts into .qm

def update_qm_files() -> None:
    files: list[str] = glob.glob(os.path.join('translations', '*.ts'))
    trans_bi_dir: str = os.path.join('src', 'lang')

    for file_name in files:
        file_name_bi: str = file_name.split('\\')[-1][:-2] + 'qm'
        subprocess.call(['pyside6-lrelease', file_name, '-qm', os.path.join(trans_bi_dir, file_name_bi)])

update_qm_files()
