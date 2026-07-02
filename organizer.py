import os
import shutil
import json
import argparse

from logger import setup_logger
from report_generator import generate_report


IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
DOCUMENT_EXTENSIONS = [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx"]
VIDEO_EXTENSIONS = [".mp4", ".mkv", ".avi", ".mov"]
MUSIC_EXTENSIONS = [".mp3", ".wav", ".aac"]


def load_config():
    with open("config.json", "r") as file:
        return json.load(file)


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def get_unique_filename(destination_folder, filename):

    name, extension = os.path.splitext(filename)

    counter = 1

    new_name = filename

    while os.path.exists(os.path.join(destination_folder, new_name)):
        new_name = f"{name}_{counter}{extension}"
        counter += 1

    return new_name


def move_file(file_path, destination_folder, logger, stats):

    try:

        create_folder(destination_folder)

        filename = os.path.basename(file_path)

        filename = get_unique_filename(destination_folder, filename)

        destination = os.path.join(destination_folder, filename)

        shutil.move(file_path, destination)

        logger.info(f"Moved: {filename}")

        print(f"Moved -> {filename}")

    except Exception as error:

        logger.error(f"Error moving {file_path}: {error}")

        print(f"Error -> {file_path}")

        stats["errors"] += 1


def organize_files(source_folder, destination_folder, logger):

    stats = {
        "images": 0,
        "documents": 0,
        "videos": 0,
        "music": 0,
        "others": 0,
        "errors": 0
    }

    if not os.path.exists(source_folder):
        print("Source folder does not exist.")
        return stats

    for filename in os.listdir(source_folder):

        file_path = os.path.join(source_folder, filename)

        if os.path.isdir(file_path):
            continue

        extension = os.path.splitext(filename)[1].lower()

        if extension in IMAGE_EXTENSIONS:

            folder = os.path.join(destination_folder, "Images")

            move_file(file_path, folder, logger, stats)

            stats["images"] += 1

        elif extension in DOCUMENT_EXTENSIONS:

            folder = os.path.join(destination_folder, "Documents")

            move_file(file_path, folder, logger, stats)

            stats["documents"] += 1

        elif extension in VIDEO_EXTENSIONS:

            folder = os.path.join(destination_folder, "Videos")

            move_file(file_path, folder, logger, stats)

            stats["videos"] += 1

        elif extension in MUSIC_EXTENSIONS:

            folder = os.path.join(destination_folder, "Music")

            move_file(file_path, folder, logger, stats)

            stats["music"] += 1

        else:

            folder = os.path.join(destination_folder, "Others")

            move_file(file_path, folder, logger, stats)

            stats["others"] += 1

    return stats


def main():

    parser = argparse.ArgumentParser(
        description="Smart File Organizer Automation Tool"
    )

    parser.add_argument(
        "--source",
        help="Source folder path"
    )

    parser.add_argument(
        "--destination",
        help="Destination folder path"
    )

    args = parser.parse_args()

    config = load_config()

    source_folder = args.source if args.source else config["source_folder"]

    destination_folder = (
        args.destination
        if args.destination
        else config["destination_folder"]
    )

    logger = setup_logger(config["log_file"])

    print("\nStarting File Organization...\n")

    logger.info("Automation Started")

    stats = organize_files(
        source_folder,
        destination_folder,
        logger
    )

    report = generate_report(
        stats,
        config["report_folder"]
    )

    logger.info("Automation Completed")

    print("\nAutomation Completed Successfully!\n")

    print("Summary")

    print("--------------------------")

    print(f"Images      : {stats['images']}")
    print(f"Documents   : {stats['documents']}")
    print(f"Videos      : {stats['videos']}")
    print(f"Music       : {stats['music']}")
    print(f"Others      : {stats['others']}")
    print(f"Errors      : {stats['errors']}")

    print(f"\nReport Generated : {report}")


if __name__ == "__main__":
    main()
    