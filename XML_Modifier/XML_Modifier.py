import os
import re
import xml.etree.ElementTree as ET

projectPath = ''
xmlFilePath = ''


def getListOfFilesPath(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()

    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFilesPath(fullPath)
        else:
            if entry.endswith(".cs") or entry.endswith(".cshtml") or entry.endswith(".config") or entry.endswith(".sql"):
                allFiles.append(fullPath)

    return allFiles


# return true if text exists in current file
def searchResourceInFile(filePath, text):
    with open(filePath, encoding="utf8", errors='ignore') as file:
        if text in file.read():
            return True


# convert list to string with new line (for display removed tags in RemovedTags.txt)
def listToString(list):

    str = ""

    # traverse in the string
    for item in list:
        str = str + item + '\n'

    # return string
    return str


fileLists = getListOfFilesPath(projectPath)

usedTags = list()
foundTags = list()
removedTags = list()
counter = 0

for file in fileLists:
    textfile = open(file, 'r', encoding="utf8", errors='ignore')
    filetext = textfile.read()
    textfile.close()
    matches = re.findall(r'\"(?:[a-zA-Z0-9_()#?.]+\.)*[a-zA-Z0-9_()#?.]+\"',
                         filetext)
    usedTags += matches

print(usedTags)

tree = ET.parse(xmlFilePath, ET.XMLParser(encoding="utf-8"))
root = tree.getroot()

for LocaleResource in root.findall('LocaleResource'):

    tagName = '"' + LocaleResource.get('Name') + '"'
    counter = counter + 1

    if tagName not in usedTags:
        root.remove(LocaleResource)
        removedTags.append(tagName)
        print(str(counter) + ' : ' + tagName + ' Removed')
    else:
        foundTags.append(tagName + ' found')
        print(str(counter) + ' : ' + tagName + ' found')

allTags = [
    e.attrib['Name'] for e in tree.iter()
    if 'Name' in e.attrib and e.tag == 'LocaleResource'
]

# generate new modified xml file in XML_Modifier.py directory
tree.write('Output.xml', encoding='utf-8')

# make new text file that contains list of removed tags of xml file
RemovedTagsFile = open('RemovedTags.txt', 'a')
RemovedTagsFile.write(str(len(removedTags)) + ' tags removed : \n')
RemovedTagsFile.write(listToString(removedTags))
RemovedTagsFile.close()

# make new text file that contains list of found tags of xml file
FoundTagsFile = open('FoundTags.txt', 'a')
FoundTagsFile.write(str(len(foundTags)) + ' tags exists in project : \n')
FoundTagsFile.write(listToString(foundTags))
FoundTagsFile.close()

input("Press Enter to exit ...")
