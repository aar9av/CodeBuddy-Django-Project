import codeforces, codechef, leetcode
from selenium_driver import driversetup


codeforces_username = 'princesharma74'
# create a selenium driver
driver = driversetup()
problems = codeforces.get_problems_solved(driver, codeforces_username)
# print(problems)