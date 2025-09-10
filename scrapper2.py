# scrapping actual websites using the requests library
from bs4 import BeautifulSoup
import requests

html_text = requests.get('https://learn.microsoft.com/en-us/answers/questions/5496387/i-meet-all-of-the-criteria-for-esu-but-i-dont-see').text

soup = BeautifulSoup(html_text, 'lxml')

def extract_question(soup):
    question_details = soup.find('div', id="question-details")
    title = question_details.find('h1', class_="title is-2").text

    description = question_details.find('div', class_="content").p.text

    
    
    return {'title':title, 'body': description}

def extract_answers(soup):
    answers = []
    answer_threads = soup.find_all('div', id="answers")
    for answer in answer_threads:
        answer_content = answer.find('p').text
        answers.append(answer_content)

    return answers

print(extract_question(soup))
print(extract_answers(soup))