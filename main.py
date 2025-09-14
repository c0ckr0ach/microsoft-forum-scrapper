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
        comment_list = []
        for comment in answer.find_all('li', id = re.compile(r'comment-\d+')):
            comment_text = comment.find('div', class_="content font-size-sm").text
            if comment_text:
                comment_list.append(comment_text)
        if content:
            answers_list.append({'content': content, 'comments': comment_list})
    
    return {'event_id': question_id,'title': title, 'description': description, 'answers': answers_list} 




site = requests.get('https://learn.microsoft.com/en-us/answers/tags/824/windows-home')

with open('htmls/index.html', 'w', encoding='utf-8') as f:
    f.write(site.text) 

with open('htmls/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

soup = BeautifulSoup(content, 'lxml')



links = extract_topic_list(soup)
with open('output_files/links.json', 'w', encoding='utf-8') as file:
    for item in links:
        json.dump(item, file, indent=4, ensure_ascii= False)

output_list =[]
for link in links:
    details = extract_question_details(link)
    output_list.append(details)
# print(output_list)
with open('output_files/topic_details.json', 'w', encoding= 'utf-8') as file:
    json.dump(output_list, file, indent=4, ensure_ascii= False)
print('end---')
print( )