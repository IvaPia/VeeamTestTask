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
        
        if os.path.isdir(file_path):                #subdirectory
            shutil.copytree(file_path, target_path)
            print(f"Copied new subdirectory {file_path} to {target_path}")
        else:
            shutil.copy2(file_path, target_path)    #file
            print(f"Copied new file {file_path} to {target_path}")
            
    #removed files or subdirectories
    for file in comp.right_only:
        file_path = os.path.join(replica, file)
        
        if os.path.isdir(file_path):                #subdirectory
            shutil.rmtree(file_path)
            print(f"Removed subdirectory {file_path}")
        else:
            os.remove(file_path)                    #file
            print(f"Removed file {file_path}")        
    
    #updated files
    for file in comp.diff_files:
        file_path = os.path.join(source, file)
        target_path = os.path.join(replica, file)
        
        shutil.copy2(file_path, target_path) 
        print(f"Updated file {file_path} to {target_path}")
        
    #updated subdirectories - include file creation and removal within subdirectory and change of files
    for subdir in comp.common_dirs:
        source_subdir_path = os.path.join(source, subdir)
        target_subdir_path = os.path.join(replica, subdir)
        sync_fun(source_subdir_path, target_subdir_path)  

#----------------------------------------------------------------------------------------------------------------

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
while(True):
    sync_fun(source_path, replica_path)

    time.sleep(sync_int)
