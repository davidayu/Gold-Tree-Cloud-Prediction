import datetime
import urllib.request
import time
import sys
import pytz
import socket


# Image Retrieval
# Download sky camera images from the web hosted repository
def download_sky_camera_images(start_time_string, 
    end_time_string):

    # 9:00 am
    start_window = '09:00:00 -0700'

    #3:00 pm 
    end_window = '15:00:00 -0700'

    window_parse = '%H:%M:%S %z'
    start_window_datetime = datetime.datetime.strptime(
        start_window, window_parse
    ).time()
    end_window_datetime = datetime.datetime.strptime(
        end_window, window_parse
    ).time()

    # Concatenate the date and time together
    start_datetime_str = "{0} {1}".format(
        start_time_string, start_window
    )
    end_datetime_str = "{0} {1}".format(
        end_time_string, end_window
    )

    # Construct datetime objects
    parse_format = '%Y-%m-%d %H:%M:%S %z'
    start_datetime_obj = datetime.datetime.strptime(
        start_datetime_str, parse_format
    )
    end_datetime_obj = datetime.datetime.strptime(
        end_datetime_str, parse_format
    )

    # How frequently the images are available for download.
    # This could increase if REC lets it - last info
    # says they asked for a quote to increase it.
    capture_interval = 5

    # Where the images are available for download
    image_url = (
        'https://cameraftpapi.drivehq.com/api/'
      + 'Camera/GetLastCameraImage.aspx?'
      + 'parentID=229229999&shareID=14125452'
      + '&time={time}')
    polite_delay = 0.5

    current_datetime_obj = start_datetime_obj
    while current_datetime_obj < end_datetime_obj:
        curr_time = current_datetime_obj.time()
        if (curr_time < start_window_datetime
                or curr_time > end_window_datetime):
            print("Ignoring", curr_time)
        else:
            # download the image
            filename = str(current_datetime_obj)
            filename = filename.replace(" ", "-")
            filename = filename.replace(":", "-")
            filename = filename[:len(filename) - 7] + '.jpg'
            utc_datetime = current_datetime_obj.astimezone(
                pytz.utc
            )
            print(utc_datetime)
            output_path = f'sky_camera_images\\{filename}'
            request_url = image_url.format(
                time=utc_datetime.strftime(
                    '%Y-%m-%d%%20%H:%M:%S'
                )
            )
            retry_retrieve(request_url, output_path)
            time.sleep(polite_delay)
        
        current_datetime_obj += datetime.timedelta(
            minutes=capture_interval
        )
    
# Reattempt to download image if error occurs
def retry_retrieve(request_url, output_path):
    retry_count = 0
    retry_max = 5
    
    print(output_path)
    while retry_count < retry_max:
        try:
            resp = urllib.request.urlopen(request_url)
            with open(output_path, 'wb') as f:
                f.write(resp.read())
            break
        except urllib.error.HTTPError as e:
            print("EXCEPTION: "
                + request_url + " " + str(e))
            continue
        except urllib.error.URLError as e:
            print("EXCEPTION: "
                + request_url + " " + str(e))
            continue
        except socket.error as e:
            print("EXCEPTION: "
                + request_url + " " + str(e))
            continue
        time.sleep(1.0)
        retry_count += 1
    if retry_count == retry_max:
        print("Unable to retrieve image. Moving on...")

# Expects date format of YYYY-MM-DD as command line args 
def main(argv):
    start = argv[0]
    end = argv[1]
    download_sky_camera_images(start, end)

# Standard boilerplate to call the main() function to begin 
# the program.
if __name__ == '__main__':
    main(sys.argv[1:])
