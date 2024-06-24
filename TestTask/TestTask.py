from genericpath import isdir
import os
import sys
import time
import filecmp
import shutil

def sync_fun(source, replica):
    #compare folders
    comp = filecmp.dircmp(source, replica)
    
    #new files or subdirectories
    for file in comp.left_only:
        file_path = os.path.join(source, file)
        target_path = os.path.join(replica, file)
        
        if os.path.isdir(file_path):             #subdirectory
            shutil.copytree(file_path, target_path)
            print(f"Copied new subdirectory {file_path} to {target_path}")
        else:
            shutil.copy2(file_path, target_path)     #file
            print(f"Copied new file {file_path} to {target_path}")
        

#arguments - folder paths, synchronization interval, log file path
if len(sys.argv) != 5:
    print("Wrong number of arguments!")
    sys.exit()

source_path = sys.argv[1]
# if not os.path.isdir(source_path):
#     print("The source folder does not exist!")
#     sys.exit()

replica_path = sys.argv[2]
# if not os.path.isdir(replica_path):
#     print("The replica folder does not exist!")
#     sys.exit()

sync_int = int(sys.argv[3])
log_file_path = sys.argv[4]

#synchronization process
#max_num = 0
while(True):
    sync_fun(source_path, replica_path)
    # max_num += 1
    # if max_num == 3:
    #     sys.exit()
    time.sleep(sync_int)
