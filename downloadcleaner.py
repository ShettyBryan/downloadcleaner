import os
import shutil
import argparse
from datetime import datetime, timedelta

parser = argparse.ArgumentParser(
    prog="downloadcleaner",
    description="Delete old files from Downloads, can specify days"
)
parser.add_argument(
    "-d",
    "--days",
    type=int,
    required=True,
    help="Specify, in days, how old the file needs to be for it to be deleted"
)

args = parser.parse_args()

DRIVE = "C:\\"
USERS = "Users\\"
USERS_DIR = os.path.join(DRIVE, USERS)

EXIT = {
    "SUCCESS": 0,
    "USERNAME_NOT_FOUND": 1,
    "DOWNLOADS_DIR_NOT_FOUND": 2,
    }


def getUsername():
    return os.getlogin()


def isFileThreeMonthsOld(filename):
    threeMonthsOld = datetime.now() - timedelta(days=args.days)
    fileTime = datetime.fromtimestamp(os.path.getmtime(filename))
    return fileTime < threeMonthsOld


def deleteOldFiles(downloadsDir):
    for root, dirs, files in os.walk(downloadsDir):
        for dir in dirs:
            if isFileThreeMonthsOld(os.path.join(root, dir)):
                try:
                    shutil.rmtree(os.path.join(root, dir))
                except OSError as e:
                    print(f"Error: {e.filename}, {e.strerror}")

        for file in files:
            if isFileThreeMonthsOld(os.path.join(root, file)):
                try:
                    os.remove(os.path.join(root, file))
                except OSError as e:
                    print(f"Error: {e.filename}, {e.strerror}")


def main():
    # Get username
    username = getUsername()

    if not username:
        return EXIT["USERNAME_NOT_FOUND"]

    DOWNLOADS_DIR = os.path.join(USERS_DIR, username, "Downloads")

    if not os.path.exists(DOWNLOADS_DIR):
        return EXIT["DOWNLOADS_DIR_NOT_FOUND"]

    deleteOldFiles(DOWNLOADS_DIR)
    return EXIT["SUCCESS"]


if __name__ == '__main__':
    main()
