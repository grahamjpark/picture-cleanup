import os
import fnmatch
import re

# Used by me to clean up pictures after I copy pictures in from my camera.
# This script will:
#   - Within the "dump" folder, delete any raw photos that don't have a corresponding jgp photo 
#   - Move raw and jpg pictures into separate folders

base_path = "./testing_data"
# _RAW_EXTENSIONS = [".raw", ",nef"]
_JPG_EXTENSIONS = [".jpg", ".jpeg"]

dump_path = os.path.join(base_path, "dump")
raw_path = os.path.join(base_path, "raw")
jpg_path = os.path.join(base_path, "jpg")

if not os.path.exists(raw_path):
    os.makedirs(raw_path)

if not os.path.exists(jpg_path):
    os.makedirs(jpg_path)
    
if os.path.isdir(dump_path):
    for picture in os.listdir(dump_path):
        if fnmatch.fnmatch(picture, '*.raw') or fnmatch.fnmatch(picture, '*.nef'):
            picture_name = re.sub('.nef$|.raw$', '', picture, flags=re.IGNORECASE)
            found = None
            for extension in _JPG_EXTENSIONS:
                path = os.path.join(dump_path, picture_name + extension)
                if os.path.exists(path):
                    found = path
                    break
            if not found:
                delete_path = os.path.join(dump_path, picture)
                os.remove(delete_path)
                print("Deleted: {}".format(delete_path))
            else:
                os.rename(path, os.path.join(jpg_path, picture_name + extension))
                os.rename(os.path.join(dump_path, picture), os.path.join(raw_path, picture))

else:
    print("ERROR: Cannot find directory: {}".format(dump_path))