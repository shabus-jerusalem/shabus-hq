from shabus import db
import csv
import os

MEMBERS_CSV_FILENAME = os.path.join(os.path.dirname(__file__), "shabus_members_2015-07-24_15-45-00.csv")

def main():
    with open(MEMBERS_CSV_FILENAME) as input_file:
        reader = csv.reader(input_file)
        for member_row in reader:
            process_row(member_row)

def process_row(member_row):
    pass

if __name__ == "__main__":
    main()
