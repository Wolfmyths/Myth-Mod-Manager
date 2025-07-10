import os
import sys
import glob
import subprocess
import xml.etree
import xml.etree.ElementTree

# Args:
# -u is to update .ts files
# -e exports .txt files with strings that need to be translated

def scrape_translations_needed(*args) -> None:

    # Update translation Files with current code
    py_file_paths: list[str] = []
    ts_file_paths: list[str] = glob.glob('.\\translations\\*.ts')

    # Put together python script paths
    for item in glob.glob('.\\src\\**', recursive=True):
        if item.endswith('.py'):
            py_file_paths.append(item)
    
    # Remove en_US because it's the default language and that file is used as a placeholder for new languages
    for s in py_file_paths:
        if s.endswith('en_US.ts'):
            py_file_paths.remove(s)
            break

    if '-u' in args:
        for ts_file in ts_file_paths:
            subprocess.call(['pyside6-lupdate', *py_file_paths, '-ts', ts_file])

    # Export missing translations
    if '-e' in args:
        messages_to_translate: dict[str:list[str]] = {}

        # Find missing translations
        for ts_file in ts_file_paths:
            key: str = os.path.basename(ts_file).split('.')[0]
            messages_to_translate[key] = []
            f: xml.etree.ElementTree.ElementTree = xml.etree.ElementTree.parse(ts_file)

            for tag in f.findall('context'):
                for tag in tag.findall('message'):
                    source: xml.etree.ElementTree.Element | None = tag.find('source')
                    translation: xml.etree.ElementTree.Element | None = tag.find('translation')
                    if source is not None and translation.get('type') is not None:
                        messages_to_translate[key].append(*source.itertext())

        # Write files
        for key in list(messages_to_translate.keys()):
            if messages_to_translate.get(key):
                with open(f'translation_needed_{key}.txt', 'w+') as f:
                    f.write('\n'.join(messages_to_translate[key]))
                    print("Wrote", key, 'at', os.path.abspath(key))

scrape_translations_needed(*sys.argv[1:])
