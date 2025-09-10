from bs4 import BeautifulSoup

with open('index.html', 'r') as file:
    content = file.read()

    soup = BeautifulSoup(content, 'lxml')
    
    # courses_html_tags = soup.find_all('h5')
    # for course in courses_html_tags:
    #     print(course.text)
    
    course_cards = soup.find_all('div', class_ = 'card')
    for cards in course_cards:
        course_name = cards.h5.text
        course_price = cards.a.text.split()[-1]

        print(course_name,' = ',course_price)
        # print(f'{course_name} = {course_price}')