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
                print(f"Matched: {result}")
    return matched_lines

def find_match(line):
    for string in MATCH_STRINGS:
        if string in line:
            if DEBUG:
                print(f"Found match:{line}")
            return C
    return None

def process_match(matched_lines):
    if matched_lines:
        for line in matched_line:
            send_to_slack(SLACK_MESSAGE_CHANNEL, line)


def send_to_slack(channel, message):
    clean_line = message.rstrip()
    slack.chat.post_message(channel, clean_line, as_user=True)
    print(f"Sent to slack: {clean_line}")

if __name__ == '__main__':
    slack = Slacker(SLACK_API_TOKEN)

    with open(f"{LOG_PATH}", 'r', encoding='latin1') as log_file:
        if PROCESS_EXISTING:
            matched_lines = process_until_EOF(log_file)
            process_match(matched_lines)
        else:
            log_file.seek(0, io.SEEK_END)

        print("Initial file read completed.")
        print(f"Now monitoring log_file for new entries every {CHECK_FREQUENCY} seconds.  Press Ctrl + C to exit!")

        current_file_size = os.stat("C:\Program Files (x86)\Steam\steamapps\common\Path of Exile\logs\Client.txt").st_size
        new_file_size = 0

        # Every x seconds, check if filesize has changed.  Read lines until EOF
        try:
            while True:
                new_file_size = os.stat(f"{LOG_PATH}").st_size
                if new_file_size > current_file_size:
                    if DEBUG:
                        print(f"Filesize changed from {current_file_size} to {new_file_size} bytes.")

                    current_file_size = new_file_size
                    matched_lines = process_until_EOF(log_file)
                    process_match(matched_lines)

                time.sleep(check_frequency)
        except KeyboardInterrupt:
            print("Monitor interrupted, exiting!")
            exit(1)
