import os
import pandas as pd

fileExcludeList = ['playground.ipynb','example.xlsx','scriptLog.xlsx','renameAndCopy.py','main.py','logHelper.py','singeFileScript.py','__pycache__']
scriptLogFileName = 'scriptLog.xlsx'
columnNames = ["FolderName","Location","OriginalFileName","PrefixIndex"]


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