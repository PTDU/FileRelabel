import os
import pandas as pd
import shutil

fileExcludeList = ['playground.ipynb','example.xlsx','scriptLog.xlsx','renameAndCopy.py','main.py','logHelper.py','singeFileScript.py','__pycache__','relabelAndMoveSingle.py','relabelAndMove.exe']
scriptLogFileName = 'scriptLog.xlsx'
columnNames = ["FolderName","Location","OriginalFileName","PrefixIndex"]

##Helper function to format the number to add 0 in front of <10 and make all into string
def formatNumberToAppend(number):
    try:
        if int(number) < 10:
            return(f'0{int(number)}')
        if int(number) >= 10:
            return(f"{int(number)}")
    except AttributeError:
        return(number)
    except ValueError:
        return(number)

##function that copies over the file and relabels them.
##it seems to crash the location when the folder location name is long
##if it fails it will rerun with generic folder named "Renamedfiles"
def copyandRename(folderLenghtIssue=False):
    try:
        df = pd.read_excel(scriptLogFileName)
        df["FormatedPreFix"] = df["PrefixIndex"].map(formatNumberToAppend)
        df["RenamedFileNames"] = df["FormatedPreFix"] +'_'+ df['OriginalFileName']
        locationValue = df['Location'][0]

        if str(locationValue) == 'nan':
            location = os.getcwd()
        else:
            location = df['Location'][0]
        print(f"Location of folder: {location}")
        if folderLenghtIssue == True:
            folderName = 'Renamedfiles'
        else: 
            folderName = str(df['FolderName'][0]) 

        try:
            folderlocation = os.path.join(location,folderName)
            os.mkdir(folderlocation)
        except OSError as error:
            print(error)

            
        for pos in df.index:
        #     print(df.iloc[pos])
            currentFileName = df["OriginalFileName"][pos]
            renamedFileName = df["RenamedFileNames"][pos]
            if str(renamedFileName) == 'nan':
                print(f"Skipping {currentFileName}, since no PrefixIndex was assigned ")
            else:    
                print(currentFileName,renamedFileName)
                src = os.path.join(os.getcwd(),currentFileName)
                dst = os.path.join(location,folderName,renamedFileName)
                shutil.copy(src,dst)
                print(f"""
                Original
                Location : {src}
                Name : {currentFileName}

                Renamed
                Location: {dst}
                Name : {renamedFileName}
                ###########################
                """)
        return(False)
    except FileNotFoundError:
        return(True)
            



#wrapper for the os.listdir function since its used frequently.
def getCurrentFileList():
    currentFiles = os.listdir('.')
    return(currentFiles)

#helper method to append data to df, has input of df, the data and position to add it to.
#top will add at -1 and increment all other index and sort again to fix ordering
#bottom just adds to last position of the df
def appendRowToDF(df,infoObj,position="bot"):
    if position == 'top':
        df.loc[-1] = infoObj
        df.index = df.index + 1
        df.sort_index(inplace=True)
    else:
        df.loc[df.shape[0]] = infoObj
    return(df)

#function that generates the log file, excludes all files starting with '.', '~' and all the files in the fileExcludeList
#if exp is found in name => assumped to be the pdf of the entry and puts it at top with a default folder name
#default folder name replaced "." with spaces and removes .pdf
def generateLogFile(df):
    fileList = getCurrentFileList()
    for file in fileList:
    #     print(file)
        if file[0] != '.' and file[0] != '~' and file not in fileExcludeList:
            if "EXP" in file:
                folderName = file.strip('.pdf').replace('.',' ').replace('-',' ')
                appendRowToDF(df,[folderName,'',file,'0'],'top')
            else:
                appendRowToDF(df,['','',file,''],'bot')
    print(f"{scriptLogFileName} Generated")
    return(df)


def doesLogFileExist():
    fileList = getCurrentFileList()
    for file in fileList:
    #     print(file)
        if file == scriptLogFileName:
            print(f"{scriptLogFileName} File Exsists,moving onto Reading and relabeling")
            return(True)
    print(f"{scriptLogFileName} not found, First Execution in folder")
    df = pd.DataFrame(columns=columnNames)
    df = generateLogFile(df)
    df.to_excel(scriptLogFileName)
    return(False)


logStatus = doesLogFileExist()

counter = 0
retry = True
if logStatus:
    while retry == True and counter <=1:
        print("Time to relabel the files and generate the new files")
        if counter == 0:
            retry = copyandRename()
            counter += 1
        else:
            print("Folder name might be too long, retrying with default folder name Renamedfiles")
            retry = copyandRename(folderLenghtIssue=True)
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
    print(f"First Execution, generated {scriptLogFileName}, Please map your Prefix and rerun to generate the relabed files.")