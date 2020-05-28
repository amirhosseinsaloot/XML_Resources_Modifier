import os
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
            if entry.endswith(".cs") or entry.endswith(".cshtml") or entry.endswith(".config") :
                allFiles.append(fullPath)
                
    return allFiles


# return true if text exists in current file
def searchResourceInFile(filePath,text):
    with open(filePath,encoding="utf8",errors='ignore') as file:
        if text in file.read():
            return True



# convert list to string with new line (for display removed tags in RemovedTags.txt)
def listToString(list):  
    
    # initialize an empty string 
    str = ""  
    
    # traverse in the string   
    for item in list:  
        str = str + item + '\n'   
    
    # return string   
    return str



fileLists = getListOfFilesPath(projectPath)

# xml.etree.ElementTree instance
tree = ET.parse(xmlFilePath,ET.XMLParser(encoding="utf-8"))
root = tree.getroot()

# false when specified tag not found in files
# true  when specified use even one file
flag = False

# list of removed tags in xml file
removedTags = []
foundTags = []

for LocaleResource in root.findall('LocaleResource'):
    tagName = LocaleResource.get('Name')
    
    for file in fileLists:
        if searchResourceInFile(file,tagName):
            flag = True
            break


    # flag remains false when specified tag 
    if flag is False:
        root.remove(LocaleResource)
        removedTags.append(tagName)
    else:
        foundTags.append(tagName + ' found in  : ' + file)


# generate new modified xml file in XML_Modifier.py directory
tree.write('Output.xml',encoding='utf-8')


# make new text file that contains list of removed tags of xml file
RemovedTagsFile = open("RemovedTags.txt", "a")
RemovedTagsFile.write(listToString(removedTags))
RemovedTagsFile.close()


# make new text file that contains list of found tags of xml file
FoundTagsFile = open("FoundTags.txt", "a")
FoundTagsFile.write(listToString(foundTags))
FoundTagsFile.close()