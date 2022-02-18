import logHelper
import renameAndCopy

logStatus = logHelper.doesLogFileExist()
if logStatus:
    print("Time to relabel the files and generate the new files")
    renameAndCopy.copyandRename()
else:
    print(f"First Execution, generated {logHelper.scriptLogFileName}, Please map your Prefix and rerun to generate the relabed files.")