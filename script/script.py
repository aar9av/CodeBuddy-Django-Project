from google_custom_module import *
from generate_message import GetMessage
from selenium_driver import driversetup
from coder import Coder
from problemClient import ProblemClient
from datetime import date
from sync_database import sync_database

# Set up the Chrome webdriver with headless mode turned on
driver = driversetup()

sheet = get_sheet('New Onboarding - The Supreme Coders (Responses)', 'The Crusaders')

sync_database()

# Get all the tuples and create Coder objects
coders = []
tuples = sheet.get_all_values()[1:]  # exclude header row
ct = 1
problem_client = ProblemClient()
for row in tuples:
    print(f'Processing row {ct}/{len(tuples)}...')
    ct += 1
    # Clean up the data
    row = [val.strip() for val in row]
    coder = Coder(*row)
    coder.fetch_solved_problems(problem_client, driver)
    coders.append(coder)

problem_client.close()
# close the driver
driver.quit()

# sort by number of problems solved
coders.sort(key=lambda x: x.total_problems, reverse=True)

# Generate the message
gm = GetMessage(coders)
gm.generate_message('output.txt')

# Define the email message
# to = ['guptajirock176@gmail.com', 'princesharma2899@gmail.com',  'priyankasahu9350@gmail.com', 'aar9av@gmail.com']
me = ['princesharma2899@gmail.com']
to = me
bcc = []
subject = 'DATE: ' + date.today().strftime("%d/%m/%Y") + ' - TheSupremeCoders'
body = open('output.txt', 'r', encoding='utf-8').read()

send_email(to, bcc, subject, body)