from bs4 import BeautifulSoup
from selenium import webdriver
import time
import csv
import sys
import datetime

def main():
    
    start_date = sys.argv[1].split('-')
    start_date = [int(x) for x in start_date]
    start_date = datetime.date(start_date[0], start_date[1], start_date[2])

    if (len(sys.argv) == 3):
        end_date = sys.argv[2].split('-')
        end_date = [int(x) for x in end_date]
        end_date = datetime.date(end_date[0], end_date[1], end_date[2])
    else:
        end_date = start_date
    delta = datetime.timedelta(days=1)

    labels = ['Date', 'Time', 'Temperature', 'Humidity', 'Condition']

    with open('wunderground_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(labels)

        while start_date <= end_date:

            url = 'https://www.wunderground.com/history/daily/us/ca/san-luis-obispo/KSBP/date/' + start_date.strftime("%Y-%m-%d")

            options = webdriver.ChromeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--ignore-ssl-errors')
            options.add_argument('--headless')
            options.add_argument('--log-level=3')
            driver = webdriver.Chrome(executable_path=r'C:\Users\David\AppData\Local\Programs\Python\Python39\chromedriver.exe', options=options)
            driver.get(url)
            html = driver.execute_script("return document.documentElement.outerHTML")
            sel_soup = BeautifulSoup(html, 'html.parser')

            daily_observation_rows = sel_soup.findAll("tr", {"class": "mat-row cdk-row ng-star-inserted"})

            while len(daily_observation_rows) == 0:
                print("Data not found. Retrying...")
                time.sleep(1)
                html = driver.execute_script("return document.documentElement.outerHTML")
                sel_soup = BeautifulSoup(html, 'html.parser')
                daily_observation_rows = sel_soup.findAll("tr", {"class": "mat-row cdk-row ng-star-inserted"})

            print(start_date.strftime("%Y-%m-%d") + " read")
            driver.close()
            
            for row in daily_observation_rows:
                row = parse_text(remove_weird_chars(row.get_text()))
                row.insert(0, start_date)

                time_of_day = row[1].split(':')
                is_am = False
                if (time_of_day[1])[len(time_of_day[1]) - 2:] == 'AM':
                    is_am = True

                if (is_am and int(time_of_day[0]) >= 8 and int(time_of_day[0]) < 12 and int(time_of_day[1][:2]) >= 30) or (not is_am and int(time_of_day[0]) < 3):
                    writer.writerow(row)
            
            start_date += delta

        
def parse_text(text):
    list = []
    temp_str = ""
    for i in range(len(text)):
        if i > 0 and text[i] == 'M' and (text[i - 1] == 'A' or text[i - 1] == 'P'):
            temp_str += text[i]
            list.append(temp_str)
            temp_str = ""
        elif len(list) == 1 and text[i] == 'F':
            temp_str += " " + text[i]
            list.append(temp_str)
            temp_str = ""
        elif len(list) == 2 and text[i] == '%':
            temp_str += " " + text[i]
            list.append(temp_str[temp_str.find('F') + 1:])
            temp_str = ""
        elif len(list) == 3 and i == len(text) - 1:
            temp_str += text[i]
            while (temp_str[0:2] != 'in'):
                temp_str = temp_str[1:]
            temp_str = temp_str[1:]
            while (temp_str[0:2] != 'in'):
                temp_str = temp_str[1:]
            list.append(temp_str[2:])
            temp_str = ""
        else:
            temp_str += text[i]
    return list

def remove_weird_chars(text):
    temp_text = ""
    for ch in text:
        if ord(ch) >= 32 and ord(ch) <= 126:
            temp_text += ch
    return temp_text

if __name__ == "__main__":
    main()

