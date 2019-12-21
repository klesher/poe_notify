 LOG_PATH = r"C:\Program Files (x86)\Steam\steamapps\common\Path of Exile\logs\Client.txt"

SLACK_API_TOKEN = "SLACK API TOKEN HERE"
SLACK_MESSAGE_CHANNEL = "@username_or_channel"



################################################
# No changes below here should be necessary for
# most use cases
################################################
# Frequency in seconds to search log for new entries.
CHECK_FREQUENCY = 5

# True = look at additional log lines, False = only parse new entries since run.
PROCESS_EXISTING = False

# Change this to look for additional matches.
MATCH_STRINGS = ("like to buy your", "disconnect")

DEBUG = False
