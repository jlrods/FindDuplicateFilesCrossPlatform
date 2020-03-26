#!/usr/bin/python
import os
import sys
import shutil
#
###########################################################################################################################################################################################
# 																			                                                                                                              #
#							                         Declare and initialize environment variables				                                                                          #
#																			                                    							   											  #
###########################################################################################################################################################################################

# Declare variable to use as root directory
root = ''
# Variable to use as temporary directory to store temp files

# Variable to reach the files name that will store the first instance of each file
global fInst
fInst = 'firstInstance.txt'
# Variable to reach the file name that will store the duplicate locations of files
global dup
dup = 'duplicates.txt'
global newFile
newFi = 'newFile.txt'
global finalDup
finalDup = 'DuplicatesFinal.txt'
# Global variable used to separate file names and location path in list of first instance and duplicate files.
global sepSymbol
sepSymbol = '?'


# Function to create a new file and populate first file name and location. The file could be the First Instance file
# or the duplicate file.
def createNewFile(storageFileName, fileName, locationDir, nextLocationDir=''):
    try:
        # Call open method with write mode to  create file and insert file name on top
        newFile = open(os.path.join(tmpDir, storageFileName), 'w', encoding='utf-8')
        # Check the nextLocationDir parameter isn't an empty string
        if nextLocationDir == '':
            newFile.write('{}{}\t{}\n'.format(fileName, sepSymbol, locationDir))
        else:
            newFile.write('{0}{1}\t{2}{1}\t{3}\n'.format(fileName, sepSymbol, locationDir, nextLocationDir))
        # Prompt user the current file has been added to firstInstance.txt file
        print('The file {} has been added in the {} file.'.format(fileName, storageFileName))
    except:
        print("An exception occurred: File {} could not be created, overwritten or closed.".format(storageFileName))
        return 3
    finally:
        newFile.close()


def appendFileAndLocation(storageFileName, fileName, locationDir, nextLocationDir=''):
    try:
        # Append to  end of first instance file
        file = open(os.path.join(tmpDir, storageFileName), 'a', encoding='utf-8')
        if nextLocationDir == '':
            file.write('{}{}\t{}\n'.format(fileName, sepSymbol, locationDir))
        else:
            file.write('{0}{1}\t{2}{1}\t{3}\n'.format(fileName, sepSymbol, locationDir, nextLocationDir))
        # Prompt user the current file has been added to firstInstance.txt file
        print('The file {} has been added in the {} file.'.format(fileName, storageFileName))
    except:
        print("An exception occurred: File {} could not be opened, overwritten or closed.".format(storageFileName))
        return 5
    finally:
        file.close()


def findFileInList(fileName, storageFile):
    # Try except block
    try:
        found = False  # Boolean flag to highlight duplicate file is already present in list
        # Call open method with append mode to add file name at the bottom of file
        file = open(os.path.join(tmpDir, storageFile), 'r', encoding='utf-8')
        # Loop through storageFile
        for line in file:
            # Check the fileName string is not in the current line
            if fileName not in line:
                continue
            # If the file name is present, carry out further check to about false duplicates.
            else:
                # Check the correct name is in the list and it's not a partial name (double check actual duplicates)
                # Split the line using the colon : symbol as delimiter, the first item in the rsplit list, must be full
                # file name (fileName)
                if line.rsplit(sepSymbol)[0] == fileName:
                    found = True
                    break
        return found
    except:
        print("An exception occurred: File {} could not be opened, searched or closed.".format(storageFile))
        return 4


def appendNewLocation(fileName, storageFileName, location):
    try:
        # Open current storage file in read mode
        oldFile = open(os.path.join(tmpDir, storageFileName), 'r', encoding='utf-8')
        # Create a new file to write new data and replace the old storage file
        newFile = open(os.path.join(tmpDir, newFi), 'w', encoding='utf-8')
        for line in oldFile:
            # Check the fileName string is not in the current line
            if fileName not in line:
                newFile.write(line)
            # If the file name is present, carry out further check to about false duplicates.
            else:
                locations = line.rsplit(sepSymbol)
                # Check the file name matches exactly the file passed in as a argument
                if locations[0] == fileName:
                    # Remove end of line scape character from current last location
                    locations[-1] = locations[-1].strip('\n')
                    # Append new location with correct tab and eol chars
                    locations.append('\t' + location + '\n')
                    # test =[line, sepSymbol, '\t'.join(location)]
                    # Create new string to hold the file name and all its location separated by sepSymbol value
                    newLine = sepSymbol.join(locations)
                    # Overwrite current line with the newLine value
                    newFile.write(newLine)
                else:
                    newFile.write(line)
                print('The file {} has been added in the {} file.'.format(fileName, storageFileName))
    except Exception as e:
        print("An exception occurred: File {} could not be opened, searched or closed.".format(storageFileName))
        print(str(e))
    finally:
        # Close both files
        oldFile.close()
        newFile.close()
        # Get rid of old file and rename new file
        os.remove(os.path.join(tmpDir, storageFileName))
        os.rename(os.path.join(tmpDir, newFi), os.path.join(tmpDir, storageFileName))


def extractFirstLocation(fileName):
    try:
        firstInstance = open(os.path.join(tmpDir, fInst), 'r', encoding='utf-8')
        for line in firstInstance:
            firstLocation = "No location defined."
            # Check the fileName string is not in the current line
            if fileName not in line:
                continue
            # If the file name is present, carry out further check to about false duplicates.
            else:
                splitLine = line.rsplit(sepSymbol)
                if splitLine[0] == fileName:
                    firstLocation = str.strip(splitLine[1])
                else:
                    continue
                return firstLocation
    except Exception as e:
        print('Error:' + e)
    finally:
        firstInstance.close()


# Function that checks for the first instance of a file. Function first checks the firstInstance.txt file exist in the
# temp folder. If not, it creates the file and records the file data (this happens when the fist file is inspected.
# If firstInstance.txt file already exists, function will look for the file name in it to determine what to do:
# add it to the firstInstance.txt file or add the extra location of duplicate.txt file. Function accepts two arguments,
# the file name to be searched and the path where the file was found.
def checkFirstInstance(tmpDir, currentDir, fileName):
    # Check the first instance file already exists withing temporary directory
    if not os.path.exists(os.path.join(tmpDir, fInst)):
        # Call function to create new file and store the file name and location
        createNewFile(fInst, fileName, currentDir)
    # In case the file FirstInstance already exists, the file name has to be searched to determine if a call to add
    # duplicate file is required or the file has to be appended to current First instance file.
    else:
        try:
            if findFileInList(fileName, fInst):
                addDuplicates(fileName, extractFirstLocation(fileName), currentDir)
            else:
                appendFileAndLocation(fInst, fileName, currentDir)
                # Append to  end of first instance file
                # firstInstanceFile = open(os.path.join(tmpDir, fInst), 'a', encoding='utf-8')
                # firstInstanceFile.write('{}{}\t{}\n'.format(fileName, sepSymbol, currentDir))
                # firstInstanceFile.close()
                # Prompt user the current file has been added to firstInstance.txt file
                # print('The file {} has been added as the first instance with that name.'.format(fileName))
        except Exception as e:
            print("An exception occurred: File {} could not be created, overwritten or closed.".format(fileName))
            print(e)
            return 4


# Function that adds an extra location to a file already present in the firstInstance file. Function first checks the
# duplicates file exist in the temp folder. If not, it creates the file and records the file data (this happens when
# the first duplicate file is found).Function accepts three arguments, the file name to be searched, path to location
# when found first and the path where the file was found last time. If file is not present in the duplicates.txt file
# the three parameters are used, otherwise only parameter 1 and 3 are used to append the latest directory.
def addDuplicates(fileName, firstLocation, nextLocation):
    # Check the duplicates file does not exist on temp location
    if not os.path.exists(os.path.join(tmpDir, dup)):
        # If first instance files does not exist, create file in temp directory tmpDir and record file name straight away
        # Call function to create new file and store the file name and location
        createNewFile(dup, fileName, firstLocation, nextLocation)
    # If it does exist, append the new data (new file name and location or just append new location to already existing
    # filename)
    else:
        # Check if file name already exists on the duplicates.txt file. If does, append new location, otherwise input
        # file name, first and current file location
        if findFileInList(fileName, dup):
            # Call method to append latest directory location for a file with more than one instance on directory tree
            appendNewLocation(fileName, dup, nextLocation)
        else:
            # Append to  end of first instance file
            appendFileAndLocation(dup, fileName, firstLocation, nextLocation)
            # duplicateFile = open(os.path.join(tmpDir, dup), 'a', encoding='utf-8')
            # duplicateFile.write('{}{}\t{}\n'.format(fileName, sepSymbol, nextLocation))
            # duplicateFile.close()
            # Prompt user the current file has been added to firstInstance.txt file
            # print('The file {} has been added as the first instance with that name.'.format(fileName))


# Recursive function to check all files and folders in the current directory (parameter passed in to function).
# The functions iterate through the directory tree, if current item is a file, the function to check if this is the
# first instance of the file is called. Otherwise, if the current item is a directory, the function will check if
# current sub-directory is empty, if it isn't, recursive call is done and current item is passed as new parameter.
def walkTree(dir, default=root):
    # Walk tree main for loop
    for (currentDir, subDirs, files) in os.walk(dir):
        # For loop to check first instance of each file in current directory currentDir
        for file in files:
            # Check first instance of file
            checkFirstInstance(tmpDir, currentDir, file)


# Function that will iterate through the duplicates.txt file line by line and split the each line into two chunks:
# The file name as a header, followed by the second part, a list of directory locations where files with same basename
# were found. This function basically extract the beginning of each line and set it as header, then iterate through the
# line and removed the locations separated by the ":" character and relocate the directory paths in subsequent lines in
# the format Location X: /path/. The output is saved in separate file called DuplicatesFinal.txt in the temp directory
def generateFinalDuplicateFile():
    try:
        # Open the duplicates file
        dupFile = open(os.path.join(tmpDir, dup), 'r', encoding='utf-8')
        # Create a new file to hold final Duplicate files information in a formatted way
        finalDupFile = open(os.path.join(tmpDir, 'DuplicatesFinal.txt'), 'w', encoding='utf-8')
        # Iterate through the old duplicate file
        for line in dupFile:
            # Extract the line and separate file name from multiple locations
            locations = str.split(line, sepSymbol)
            # Write the file name on the Final Duplicates file
            finalDupFile.write(locations[0] + ':\n')
            # Make the locations object an iterator object so next() function is available
            locations = iter(locations)
            locations.__next__()
            # Declare and initialize counter to display current file location number
            i = 1
            # Inner for loop to iterate through all the file locations
            for location in locations:
                # Print formatted data for the current location
                finalDupFile.write('\t\tLocation {}:\t{}\n'.format(i, location))
                # Increase the counter
                i += 1
        return 0
    except Exception as e:
        print('Error: ' + e)
        return 1
    finally:
        dupFile.close()
        finalDupFile.close()


def FindDuplicateFiles():
    # Check the number of parameters passed in is correct. The script can accept one or no argument, other than that
    # must report an error.
    global tmpDir
    if len(sys.argv) <= 2:
        # Check if there's only one argument on argv, which means the default root directory should be assigned
        if len(sys.argv) == 1:
            # Set variable to use as root directory and temporary directory for Windows
            if sys.platform == 'win32':
                root = os.path.join('C:\\Users\\', os.environ['USERNAME'], 'Documents')
                tmpDir = os.path.join('C:\\Users\\', os.environ['USERNAME'], 'AppData', 'Local', 'Temp',
                                      'FindDuplicates')
            else:
                # otherwise, assume Linux base OS. Temporary folder path will remain ad defined on top of script
                root = '~'
                tmpDir = os.path.join('tmp,FindDuplicateFiles')
        else:
            # If argv length is not 1, then it's 2 as it was already checked to be less than 2.
            # This means a search path was passed in as parameter.
            root = sys.argv[1]
            print("The root directory for the current search is " + root)
        # Prompt user the seed for walking the directory tree
        print("The directory {} is not empty. It has {} files and folders in total and will be walked to search "
              "duplicate files.".format(root, len(os.listdir(root))))
        # Check the current root directory isn't empty
        if len(os.listdir(root)) > 0:
            # Check the temp directory exists. If not, create a temp directory to store temporary working files
            if os.path.isdir(tmpDir):
                # Print the temp directory to be used already exists
                print("The temporary directory path: {} already exists.".format(tmpDir))
            else:
                # If temporary directory does not exist, create it and prompt user
                os.mkdir(tmpDir)
                print("The temporary directory path: {} has been created for processing the search.".format(tmpDir))

            # Once the temp directory is created, start recursive search for duplicate files by calling recursive
            # function to iterate through the file tree.
            # Pass the root directory as initial seed for the iterative search.
            walkTree(root)
            # Check if script found any duplicate files by checking the duplicates files exist and is not empty
            if os.path.exists(os.path.join(tmpDir, dup)):
                # Once the search process is done, the duplicates.txt file must be presented in better looking format.
                # The proposed solution consists of calling a function that will iterate through the file line by line
                # and split the line into two chunks:The file name as a header, followed by the second part, a list of
                # directory locations where files with same basename were found. Call method to generate formatted
                # Duplicates.txt file and call program to display list of duplicate files
                if(generateFinalDuplicateFile() == 0):
                    print('The Final Duplicates file has been generated.')

                # Move FindDuplicateFiles file to root directory
                os.replace(os.path.join(tmpDir, finalDup), os.path.join(root, finalDup))
                print('The {} file has been moved to this folder: {} and is to be displayed on the notepad.'.format(finalDup, root))
                input('Please, press any key to display the list of duplicates found on the {} directory.'.format(root))
                # Display presentable duplicates file
                if sys.platform == 'win32':
                    os.system("start " + os.path.join(root, finalDup))
                else:
                    os.system("xdg-open " + os.path.join(root, finalDup))
            else:
                # If no duplicate files is found, means there are no duplicates in the specified directory
                print("No duplicate files have been found on the {} directory or sub-directories!".format(root))
            # Remove temporary files
            shutil.rmtree(tmpDir)
            #os.rmdir(tmpDir)
            print("Temporary files have been removed!")
            input("Press any key to finish... Good bye!")
            return 0
        else:
            print("The directory {} is empty. It has no files or folders in it.".format(root))
            input()
            return 2
    else:
        # Display error message and invite user to call the script with correct number of parameters
        print("Error. Wrong number of parameters passed in. This script can accept one or no parameters.")
        print("Please, try again.")
        return 1


if __name__ == '__main__':
    FindDuplicateFiles()
