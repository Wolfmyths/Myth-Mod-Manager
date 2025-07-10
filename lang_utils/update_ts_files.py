import xml.etree
import xml.etree.ElementTree
import sys

# First arg is the file that has the translations MAKE SURE TRANSLATIONS HAVE A NEWLINE BETWEEN THEM
# Second arg is the ts file to update translations

# MAKE SURE TO NOT HAVE EDITED THE TS FILE DURING TRANSLATION THE TRANSLATIONS WOULD BE OUT OF ORDER

def fill_missing_translations(ts_file, translation_file) -> None:

    translations: list[str] = None

    with open(translation_file, 'r', encoding='utf8') as f:
        translations = f.readlines()

    ts_hand: xml.etree.ElementTree.ElementTree = xml.etree.ElementTree.parse(ts_file)

    index = 0
    for tag in ts_hand.findall('context'):
        for tag in tag.findall('message'):
            translation: xml.etree.ElementTree.Element | None = tag.find('translation')
            if translation.get('type') is not None:
                translation.text = translations[index].rstrip()
                translation.attrib.pop('type')
                index += 1

    with open(ts_file, 'wb') as f:
        f.write(xml.etree.ElementTree.tostring(ts_hand.getroot(), encoding='utf-8'))

fill_missing_translations(sys.argv[1], sys.argv[2])