import login
import json
import csv

courses = login.execute()

#? newline ký tự đầu dầu khi new line
with open('courses.csv', mode='w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(['id', 'title', 'url', 'is_paid', 'price', 'price_detail'])

    for course in courses['results']:
        writer.writerow([
            course['id'],
            course['title'],
            course['url'],
            course['is_paid'],
            course['price'],
            course['price_detail']
        ])