from __future__ import annotations

import os
import json
import xml.etree.ElementTree as et
import logging

from PySide6.QtCore import QVersionNumber

logging.getLogger(__file__)

def __loadXML(modPath: str) -> et.ElementTree[et.Element[str]] | None:

    xmlName = 'main.xml'

    xmlPath: str = os.path.join(modPath, xmlName)

    logging.debug('Checking xml file of %s', os.path.basename(modPath))
    
    try:
        if os.path.exists(xmlPath):
            xml = et.parse(xmlPath)
            return xml
        
    except Exception as e:
        logging.error('Something went wrong parsing an xml file in %s:\n%s', os.path.basename(modPath), str(e))

def __parseVersion(version: str | None) -> QVersionNumber | None:

    logging.debug('Parsing %s', version)

    if version is None:
        return
    
    removeChars = ('v', 'V')
    try:
        if version.startswith(removeChars):
            version = version[1:]
        if version.endswith(removeChars):
            version = version[:-1]
        
        version_qver = QVersionNumber.fromString(version)

    except Exception as e:
        logging.error('Something went wrong in __parseVersion() parsing version %s: %s', version, str(e))
        version_qver = None
    
    return version_qver

def findModworkshopAssetID(modPath: str) -> str:
    '''Finds the AssetID of a modworkshop mod if it can'''

    assetID = ''

    xml: et.ElementTree[et.Element[str]] | None = __loadXML(modPath)

    if xml is None:
        return assetID

    assetUpdates: et.Element | None = xml.find('AssetUpdates')

    if assetUpdates is not None:

        modworkshop: bool = assetUpdates.attrib.get('provider') == 'modworkshop'
        assetID: str = assetUpdates.attrib.get('id', '')

        if modworkshop and assetID:
            return assetID
    
    return assetID

def findModVersion(modPath: str) -> QVersionNumber | None:
    '''Finds the mod version if it can by parsing `main.xml` and `mod.txt`'''
    try:

        version: str | None = None

        xml: et.ElementTree[et.Element[str]] | None = __loadXML(modPath)

        txtName = 'mod.txt'
        txtPath: str = os.path.join(modPath, txtName)

        if xml is not None:

            assetUpdates: et.Element | None = xml.find('AssetUpdates')

            if assetUpdates is not None and assetUpdates.attrib.get('version'):

                version = assetUpdates.attrib.get('version')

            elif xml.getroot().get('version'):
                version = xml.getroot().get('version')

        else:
            
            if os.path.exists(txtPath):
                logging.debug('Checking txt file of %s', os.path.basename(modPath))
                with open(txtPath, 'r') as f:
                    for line in f.readlines():
                        line: str = line.strip()

                        if line.startswith('"version"'):

                            if line.endswith(','):
                                line = line.removesuffix(',')

                            data: dict[str, str] = json.loads('{{{line}}}'.format(line=line))

                            version = data.get('version')

                            break
      
        return __parseVersion(version)
    
    except Exception as e:

        logging.error('Something happened in findModVersion with %s: %s', os.path.basename(modPath), e)
        return None

    
