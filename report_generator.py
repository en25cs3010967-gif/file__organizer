import os
from datetime import datetime


def generate_report(stats, report_folder):

    if not os.path.exists(report_folder):
        os.makedirs(report_folder)

    report_path = os.path.join(report_folder, "report.txt")

    with open(report_path, "w") as file:

        file.write("=" * 50 + "\n")
        file.write("SMART FILE ORGANIZER REPORT\n")
        file.write("=" * 50 + "\n\n")

        file.write(f"Generated On : {datetime.now()}\n\n")

        file.write(f"Images      : {stats['images']}\n")
        file.write(f"Documents   : {stats['documents']}\n")
        file.write(f"Videos      : {stats['videos']}\n")
        file.write(f"Music       : {stats['music']}\n")
        file.write(f"Others      : {stats['others']}\n")
        file.write(f"Errors      : {stats['errors']}\n")

        file.write("\n")
        file.write("=" * 50)