# TODO: Add these inline - believe I was having issues.
# logPath = r"C:\Program Files (x86)\Steam\steamapps\common\Path of Exile\logs\"
# logName = "Client.txt"
DEBUG = False

# True = look at additional log lines, False = only parse new entries since run.
process_existing = False

# Change this to look for additional matches.
match_strings = ("like to buy your", "disconnect")

# Frequency in seconds to search log for new entries.
check_frequency = 5
slack_api_token = "SLACK API TOKEN HERE"
slack_message_channel = "@username_or_channel"
