import os
import sys

#arguments - folder paths, synchronization interval, log file path
if len(sys.argv) != 5:
    print("Wrong number of arguments!")
    sys.exit()

source = sys.argv[1]
# while not os.path.isdir(source):
#     print("The source folder does not exist!")
#     sys.exit()

replica = sys.argv[2]
# while not os.path.isdir(replica):
#     print("The replica folder does not exist!")
#     sys.exit()

sync_int = sys.argv[3]
log_file_path = sys.argv[4]
