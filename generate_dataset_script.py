
import os
import csv
import datetime

def main():
    start_date = "2019-05-23"
    end_date = "2019-05-26"

    start_datetime = datetime.date(int(start_date[:4]), int(start_date[5:7]), int(start_date[8:]))
    end_datetime = datetime.date(int(end_date[:4]), int(end_date[5:7]), int(end_date[8:]))
    delta = datetime.timedelta(days=1)


    # write meteoblue data to training_data.csv
    dates = []

    while True:
        if start_datetime > end_datetime:
            break
        dates.append(start_datetime)
        start_datetime += delta

    times = ['0900', '1000', '1100', '1200', '1300', '1400', '1500']

    with open('training_data.csv', 'w', newline='') as wfile:
        writer = csv.writer(wfile)
        with open('meteoblue_data.csv') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if (row[0] == 'variable' or row[0] == 'unit' or row[0] == 'level'):
                    writer.writerow(row)
                date_time = row[0]
                date = date_time[:8]
                if (represents_int(date)):
                    date = datetime.date(int(date[:4]), int(date[4:6]), int(date[6:]))
                    time = date_time[9:]
                    
                    if date in dates and time in times:
                        writer.writerow(row)

    # TO-DO: download relevent cloud images, calculate cloud cover at the time and after 5 minutes, 10 minutes and write the data to training_data.csv


def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    main()