import logHelper
import renameAndCopy

logStatus = logHelper.doesLogFileExist()

counter = 0
retry = True
if logStatus:
    while retry == True and counter <=1:
        print("Time to relabel the files and generate the new files")
        if counter == 0:
            retry = renameAndCopy.copyandRename()
            counter += 1
        else:
            print("Folder name might be too long, retrying with default folder name Renamedfiles")
            retry = renameAndCopy.copyandRename(folderLenghtIssue=True)
            if retry == False:
                counter += 1
    print("#############################################################################")
    if retry == True and counter >1 :
        print("Something is not working correctly, the script failed to relabel and move")
        print("Please move all files to shorter path and try again.")
        print("Before")
        print(r"C:\Users\example\Downloads\FileRelabel\EXP20005199 VAL 0149423  Process Parameter Study A Chromatography Runs   Accepted at 2021 04 13T14 26 53Z")
        print("After")
        print(r"C:\Users\example\Desktop\FileRelabel")
    else:
        if counter == 2:
            print("However, Had to use default Folder Name: 'Renamedfiles', given/default folder name was too long.")
        else:
            print("Succesfully Renamed and Copied to folder defined in excel file.")
    
            

else:
    print(f"First Execution, generated {logHelper.scriptLogFileName}, Please map your Prefix and rerun to generate the relabed files.")