import pandas as pd
import os
import shutil
from logHelper import scriptLogFileName

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
            