import os
temp_dir = "tests/data/temp/"
if not os.path.isdir(temp_dir) :
    try:
        os.mkdir(temp_dir)
    except OSError:
        print ("Creation of the directory %s failed" % temp_dir)
