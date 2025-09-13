import requests
from bs4 import BeautifulSoup
import re
import json

def extract_topic_list(soup):
    topic_links = []


    for topic in soup.find_all('h2', class_ = 'title is-6 margin-bottom-xxs'):
        topic_links.append('https://learn.microsoft.com' + topic.a['href'])

    return topic_links


def extract_question_details(question_link):
    thread = requests.get(question_link)

    with open('htmls/thread.html', 'w', encoding='utf-8') as f:
        f.write(thread.text)

    with open('htmls/thread.html', 'r', encoding='utf-8') as f:
        thread = f.read()

    soup = BeautifulSoup(thread, 'lxml')

    question_id = re.search(r'/questions/(\d+)/', question_link).group(1)

    title = soup.find('h1', class_="title is-2").text

    description = soup.find('div', class_="content margin-top-xxs").text
    
    answers_list = []
    for answer in soup.find_all('li', id= re.compile(r'answer-\d+')):
        content = answer.find('div', class_='content').text
        answers_list.append(content)
    
    
    return {'event_id': question_id,'title': title, 'description': description, 'answers': answers_list} 




site = requests.get('https://learn.microsoft.com/en-us/answers/tags/824/windows-home')
# create a folder named htmls in the current directory before running this code
with open('htmls/index.html', 'w', encoding='utf-8') as f:
    f.write(site.text) 

with open('htmls/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

soup = BeautifulSoup(content, 'lxml')



data = extract_topic_list(soup)
with open('output_files/links.json', 'w', encoding='utf-8') as file:
    for item in data:
        json.dump(item, file)
        file.write('\n')

details = extract_question_details('https://learn.microsoft.com/en-us/answers/questions/5549812/installing-windows-11-fails-with-multiple-bsod-err')
print(details)
print('end---')
print( )