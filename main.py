import sys, os, time, io
from config import *
from slacker import Slacker

def process_until_EOF(file):
    matched_lines = []
    for log_line in log_file:
        result = find_match(log_line)
        if result:
            matched_lines.append(result)
            if DEBUG:
                print("Matched: {}".format(result))
    return matched_lines

def find_match(line):
    for string in match_strings:
        if string in line:
            if DEBUG:
                print("Found match:{}".format(line))
            return line
    return None

def process_match(matches):
    if matches:
        for entry in matches:
            send_to_slack(slack_message_channel, entry)

def send_to_slack(channel, message):
    clean_line = message.rstrip()
    slack.chat.post_message(channel, clean_line, as_user=True)
    print("Sent to slack: {}".format(clean_line))

if __name__ == '__main__':
    slack = Slacker(slack_api_token)

    with open("C:\Program Files (x86)\Steam\steamapps\common\Path of Exile\logs\Client.txt", 'r', encoding='latin1') as log_file:
        if process_existing:
            matched_lines = process_until_EOF(log_file)
            process_match(matched_lines)
        else:
            log_file.seek(0, io.SEEK_END)

        print("Initial file read completed.")
        print("Now monitoring log_file for new entries every {} seconds.  Press Ctrl + C to exit!".format(check_frequency))

        current_file_size = os.stat("C:\Program Files (x86)\Steam\steamapps\common\Path of Exile\logs\Client.txt").st_size
        new_file_size = 0

        # Every x seconds, check if filesize has changed.  Read lines until EOF
        try:
            while True:
                new_file_size = os.stat("C:\Program Files (x86)\Steam\steamapps\common\Path of Exile\logs\Client.txt").st_size
                if new_file_size > current_file_size:
                    if DEBUG:
                        print("Filesize changed from {} to {} bytes.".format(current_file_size, new_file_size))

                    current_file_size = new_file_size
                    matched_lines = process_until_EOF(log_file)
                    process_match(matched_lines)

                time.sleep(check_frequency)
        except KeyboardInterrupt:
            print('Monitor interrupted, exiting!')
            exit(1)
