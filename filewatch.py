import src.sqlite as db
from src.checksum import *
from os import listdir
from os.path import isfile, join
import time

def main():
    """Main module

    
    """
    __EXAMPLE_FOLDER__ = "example/"
    db.init()

    print("Deamon ready")

    while True:
        files = [f for f in listdir(__EXAMPLE_FOLDER__) if isfile(join(__EXAMPLE_FOLDER__, f))]
        db_files = db.select_filename()
        for file in files:
            # TO DO : PENSER A FAIRE LES FICHIERS SUPPRIME
            if(db_files.index(file) >= 0):
                # Delete all files existing in folder and database
                del db_files[db_files.index(file)]

            # File exist in db
            checksum = checksum_file(__EXAMPLE_FOLDER__ + file)
            if(db.count(file) > 0):
                if(db.select(file)[2] != checksum):
                    print("> File changed", file)
                    if(db.update_signature(file, checksum) == False):
                        print("(!) Error while updating database")
            else:
                print("> New file detected", file)
                db.write(file, __EXAMPLE_FOLDER__, checksum)
                
        print("new db file", db_files)

        # Detect file removed here
        for deleted in db_files:
            print(">", deleted, "removed")
        time.sleep(3.5) # in sec
    

if __name__ == '__main__':
    main()