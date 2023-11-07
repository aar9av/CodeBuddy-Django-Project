import time
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re

def get_problems_solved(driver, username):
    # Extract the username from the LeetCode ID
    # pattern = r'https://leetcode.com/([^/]+)/?'
    # username = re.search(pattern, self.leetcode_id).group(1)
    problems_leetcode = []
    driver.get(url)
    time.sleep(3)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract the titles of the most recent problems solved
    div = soup.find_all('div', attrs={'data-title': True})
    for i in div:
        children = i.findChildren('span')
        pattern = r'^(a\ minute\ ago|a\ few\ seconds\ ago|an\ hour\ ago|\d+\ hours\ ago|\d+\ minutes\ ago)$'
        match = re.search(pattern, children[1].text)
        # concatenate the link with the base url
        if match:
            submission_link = f"https://leetcode.com{i.parent['href']}"
            problem_link = f"https://leetcode.com/problems/{i['data-title'].lower().replace(' ', '-')}/"
            submission_id = i.parent['href'].split('/')[-2]
            problems_leetcode.append(Problem(problem_client,  i['data-title'], problem_link, submission_link, submission_id, 'Leetcode', scholar_number ))
        else:
            break

    return problems_leetcode