# FileRelabel

Purpose:
To Help PurDev PV team relabel with prefix and organize Benchling entry exports

How to use:
The script has two stages (1) directory file list generation -> (2) copy and relabel.

    0. Move the py file(s) or exe into folder and execute. 3 options below.
        - Copy "relabelAndMoveSingle.py", its just combined file from 3 files. CMD Execute ->  "python relabelAndMoveSingle.py"
        - Copy "main.py", "logHelper.py" and "renameAndCopy.py" to working directly. CMD Execute ->  "python main.py"
        - Copy over "relabelAndMove.exe".

    1. First execution will generate current directly filename content into file called "scriptLog.xlsx". The file has 4 columns:"FolderName","Location","OriginalFileName","PrefixIndex".

    2. This is where the user can define: FolderName(optional), Location(optional) and Prefixindex(required - integer). Rows with missing prefixindex value will be ignored.

    3. Second execution will pull the prefix to add from the file and copy and rename the file according to the information in excel sheet.

Notes:
-Single EXE file should work on any windows PC that does not have python installed. However it will take a moment to load vs the py file will execute instantly. If possible use the py file.

    - If the file path of the folder is too large, specially nested folders of long names. The parsing for directory breaks. If this happens the script is written to retry and export into a default folder in the same location as the script file.

    -Currently only pre-appending index number only. (Upgrade to include other information?)

    -if prefixindex is blank for a file, that file is ignored.

MAC OS Notes:

On mac before you can use the script you need to install dependencies for the script and it will need to be run with the file relabelAndMoveSingle.py. Below are the steps and commands you need to run in your terminal.

    -Open Terminal by via finder or spotlight search.
    -Navigate to the directory where FileRelabel is downloaded.(Use cd cmd - example below of navigating from route to my FileRelabel on my Desktop)
        -Can do it in one cmd or Multiple:
        -Single:
        -cd Desktop/FileRelabel
        -Multiple:
        -cd Desktop
        -cd FileRelabel
    -Install dependencies using pip(python package manager)
        -pip3 install -r requirements.txt
    -Navigate to were entry files you want to relabel are located(relabelAndMoveSingle.py should be copied to this already)
        -python3 relabelAndMoveSingle.py
        -Use this command as you would inplace of the exe file in windows machine.
