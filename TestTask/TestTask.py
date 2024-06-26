import os
import sys
import time
import filecmp
import shutil
import datetime

#sync for new files and subdirectories
def sync_new(source, replica, log_file, comp):
    
    for file in comp.left_only:
        file_path = os.path.join(source, file)
        target_path = os.path.join(replica, file)
        
        if os.path.isdir(file_path):                    #subdirectory
            shutil.copytree(file_path, target_path)
            print(f"Copied new subdirectory {file_path} to {target_path}")
            log_file.write(f"Copied new subdirectory {file_path} to {target_path} at {datetime.datetime.now()}\n")
        else:
            shutil.copy2(file_path, target_path)    #file
            print(f"Copied new file {file_path} to {target_path}")
            log_file.write(f"Copied new file {file_path} to {target_path} at {datetime.datetime.now()}\n")

#sync for removed files and subdirectories
def sync_removed(replica, log_file, comp):
    
    for file in comp.right_only:
        file_path = os.path.join(replica, file)
        
        if os.path.isdir(file_path):                    #subdirectory
            shutil.rmtree(file_path)    
            print(f"Removed subdirectory {file_path}")
            log_file.write(f"Removed subdirectory {file_path} at {datetime.datetime.now()}\n")
        else:        
            os.remove(file_path)                    #file
            print(f"Removed file {file_path}")
            log_file.write(f"Removed file {file_path} at {datetime.datetime.now()}\n")

#sync for updated files
def sync_updated_files(source, replica, log_file, comp):
    
    for file in comp.diff_files:
        file_path = os.path.join(source, file)
        target_path = os.path.join(replica, file)
        
        shutil.copy2(file_path, target_path)           
        print(f"Updated file {file_path} and copied to {target_path}")
        log_file.write(f"Updated file {file_path} and copied to {target_path} at {datetime.datetime.now()}\n")

#sync source and replica directories
def sync_dirs(source, replica, log_file):
    
    #compare folders
    comp = filecmp.dircmp(source, replica)
    
    #new files or subdirectories
    sync_new(source, replica, log_file, comp)
            
    #removed files or subdirectories
    sync_removed(replica, log_file, comp)
    
    #updated files
    sync_updated_files(source, replica, log_file, comp)
        
    #updated subdirectories - include file creation and removal within subdirectory and change of files
    for subdir in comp.common_dirs:
        source_subdir_path = os.path.join(source, subdir)
        target_subdir_path = os.path.join(replica, subdir)
        sync_dirs(source_subdir_path, target_subdir_path, log_file)  
        
    #flush data to log file
    log_file.flush()

#----------------------------------------------------------------------------------------------------------------

#arguments - folder paths, synchronization interval, log file path
if len(sys.argv) != 5:
    print("Wrong number of arguments!")
    sys.exit()

source_path = sys.argv[1]
if not os.path.isdir(source_path):
    print("The source folder does not exist!")
    sys.exit()

replica_path = sys.argv[2]
if not os.path.isdir(replica_path):
    print("The replica folder does not exist!")
    sys.exit()

sync_int = int(sys.argv[3])

log_file_path = sys.argv[4]
if not (os.path.isdir(log_file_path) and os.access(log_file_path, os.W_OK)):
    print("The log file path does not exist!")
    sys.exit()

#create a log file
f = open(os.path.join(log_file_path, "sync_log_file.txt"), "w")
f.write(f"Folder synchronization between source {source_path} and replica {replica_path} started at {datetime.datetime.now()}\n\n")
print(f"Folder synchronization between source {source_path} and replica {replica_path} started at {datetime.datetime.now()}\n")

#synchronization process
while(True):
    try:
        sync_dirs(source_path, replica_path, f)
    except FileNotFoundError as e:
        print(f"FileNotFoundError: {e}\nSynchronization failed, trying again in next step.")
    except FileExistsError as e:
        print(f"FileExistsError: {e}\nSynchronization failed, trying again in next step.")
    except PermissionError as e:
        print(f"PermissionError: {e}\nSynchronization failed, trying again in next step.")
    except OSError as e:
        print(f"OSError: {e}\nSynchronization failed, trying again in next step.")

    time.sleep(sync_int)
