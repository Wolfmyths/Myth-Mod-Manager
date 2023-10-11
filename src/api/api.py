import os
import json
import xml.etree.ElementTree as et
import logging

from semantic_version import Version

logging.getLogger(__file__)

def __loadXML(modPath: str) -> et.ElementTree | None:

    xmlName = 'main.xml'

    xmlPath = os.path.join(modPath, xmlName)

    xml = None

    logging.debug('Checking xml file of %s', os.path.basename(modPath))
    
    try:
        if os.path.exists(xmlPath):
            xml = et.parse(xmlPath)
    except Exception as e:
        logging.error('Something went wrong parsing an xml file in %s:\n%s', os.path.basename(modPath), str(e))
    
    return xml

def __parseVersion(version: str) -> Version | None:

    logging.debug('Parsing %s', version)

    if version is None:
        return
    
    removeChars = ('v', 'V')
    try:
        if version.startswith(removeChars):
            version = version[1:]
        if version.endswith(removeChars):
            version = version[:-1]
        
        version = Version.coerce(version)

    except Exception as e:
        logging.error('Something went wrong in __parseVersion() parsing version %s: %s', version, str(e))
        version = None
    
    return version

def findModworkshopAssetID(modPath: str) -> str | None:
    '''Finds the AssetID of a modworkshop mod if it can'''

    xml = __loadXML(modPath)

    if xml is None:
        return

    assetUpdates = xml.find('AssetUpdates')

    if assetUpdates is not None:

        modworkshop = assetUpdates.attrib.get('provider') == 'modworkshop'
        assetID = assetUpdates.attrib.get('id')

        if modworkshop and assetID:
            return assetID

def findModVersion(modPath: str) -> Version | None:
    '''Finds the mod version if it can by parsing `main.xml` and `mod.txt`'''

    version: str | None = None

    xml = __loadXML(modPath)

    txtName = 'mod.txt'
    txtPath = os.path.join(modPath, txtName)

    if xml is not None:

        assetUpdates = xml.find('AssetUpdates')

        if assetUpdates is not None and assetUpdates.attrib.get('version'):

            version = assetUpdates.attrib.get('version')

        elif xml.getroot().get('version'):
            version = xml.getroot().get('version')

    else:
        
        if os.path.exists(txtPath):
            logging.debug('Checking txt file of %s', os.path.basename(modPath))
            with open(txtPath, 'r') as f:
                for line in f.readlines():
                    line = line.strip()

                    if line.startswith('"version"'):

                        if line.endswith(','):
                            line = line.removesuffix(',')
                        try:
                            data: dict = json.loads('{{{line}}}'.format(line=line))
                        except json.decoder.JSONDecodeError as e:
                            logging.error('Something went wrong converting a mod version into a dictionary in %s:\n%s', txtPath, str(e))

                        version = data.get('version')

                        break


    return __parseVersion(version)
