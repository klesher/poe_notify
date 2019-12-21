import sys, os, time, io
from config import *
import re
import requests

if PLATFORM == "slack":
    from slacker import Slacker

def process_until_EOF(file):
    matched_lines = []
    for log_line in log_file:
        result = find_match(log_line)
        if result:
            matched_lines.append(result)

    return matched_lines

def find_match(line):
    matches_re = re.compile("|".join(MATCH_REGEXES))

    if matches_re.search(line):
        if DEBUG:
            print(f"Found match:{line}")
        return line
    return None

def process_matches(matched_lines):
    if matched_lines:
        for line in matched_lines:
            line = clean_line(line)

            if PLATFORM == "discord":
                send_to_discord(DISCORD_BOT_NAME, DISCORD_MENTION_ID, line)
            elif PLATFORM == "slack":
                send_to_slack(SLACK_MESSAGE_CHANNEL, line)
            else:
                printf("No valid platform detected.")
                exit(1)

def clean_line(line):
    line = line.rstrip()

    # Check if this was a message being sent to us
    index = line.find("@From")
    if index != -1:
        return line[index:]

    return line


def send_to_slack(channel, message):

    slack.chat.post_message(channel, clean_line, as_user=True)
    print(f"Sent to slack: {clean_line}")

def send_to_discord(bot_name, mention_id, message):
    clean_line = message.rstrip()

    payload = {
        "username": bot_name,
        "content": f"{message} - <@{mention_id}>"
    }

    r = requests.post(DISCORD_WEBHOOK, json = payload)

    if r.status_code == 204:
        print(f"Sent to Discord: {payload['content']}")
        return True

    r.raise_for_status()
    return False

if __name__ == '__main__':
    if PLATFORM == "slack":
        slack = Slacker(SLACK_API_TOKEN)

    with open(f"{LOG_PATH}", 'r', encoding='latin1') as log_file:
        if PROCESS_EXISTING:
            matched_lines = process_until_EOF(log_file)
            process_matches(matched_lines)
        else:
            log_file.seek(0, io.SEEK_END)

        print("Initial file read completed.")
        print(f"Now monitoring log_file for new entries every {CHECK_FREQUENCY} seconds.  Press Ctrl + C to exit!")

        current_file_size = os.stat(LOG_PATH).st_size
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
                    process_matches(matched_lines)

                time.sleep(CHECK_FREQUENCY)
        except KeyboardInterrupt:
            print("Monitor interrupted, exiting!")
            exit(1)
