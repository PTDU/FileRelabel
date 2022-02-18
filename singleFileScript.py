import os
import pandas as pd
import shutil
columnNames = ["FolderName","Location","OriginalFileName","PrefixIndex"]
fileExcludeList = ['playground.ipynb','example.xlsx','scriptLog.xlsx']
scriptLogFileName = 'scriptLog.xlsx'

#wrapper for the os.listdir function since its used frequently.
def getCurrentFileList():
    currentFiles = os.listdir('.')
    return(currentFiles)

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

def appendRowToDF(df,infoObj,position="bot"):
    if position == 'top':
        df.loc[-1] = infoObj
        df.index = df.index + 1
        df.sort_index(inplace=True)
    else:
        df.loc[df.shape[0]] = infoObj
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
def copyandRename():
    df = pd.read_excel(scriptLogFileName)
    df["FormatedPreFix"] = df["PrefixIndex"].map(formatNumberToAppend)
    df["RenamedFileNames"] = df["FormatedPreFix"] +'_'+ df['OriginalFileName']
    locationValue = df['Location'][0]
    if str(locationValue) == 'nan':
        location = os.getcwd()
    else:
        location = df['Location'][0]
    print(f"Location of folder: {location}")
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
            
logStatus = doesLogFileExist()
if logStatus:
    print("Time to relabel the files and generate the new files")
    copyandRename()
else:
    print(f"First Execution, generated {scriptLogFileName}, Please map your Prefix and rerun to generate the relabed files.")