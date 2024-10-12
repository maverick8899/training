import config
import logout
import get_courses
import requests
import os
# from bs4 import BeautifulSoup
# from urllib.parse import urlencode


def execute():
    session = requests.Session()
    response = session.get(config.WEB_URL)

    login_data = {
        'email': config.EMAIL,
        'password': config.PASSWORD,
        'csrfmiddlewaretoken': config.CSRF_TOKEN
    }
    # print(urlencode(login_data))
    headers = {
        'Referer': config.WEB_URL,
        'User-Agent': 'Popular browser\'s user-agent'
    }
    cookies = {
        'csrftoken': config.CSRF_TOKEN
    }

    login_response = session.post(
        config.LOGIN_API, data=login_data, headers=headers, cookies=cookies)

    access_token = login_response.cookies.get('access_token')

    print("📝 login_response: ", login_response.text)
    print("📝 access_token: ", access_token)
    print("📝 status_code: ", login_response.status_code)

    courses = ''
    if login_response.status_code == 200 and access_token != None:
        print("✅✅✅ Login successfully ✅✅✅ \n")
        courses = get_courses.execute(session, headers, cookies={
                                      **cookies, 'access_token': access_token}, api=config.GET_COURSE_API)
        logout.execute(session, headers, cookies={
                       **cookies, 'access_token': access_token}, api=config.LOGOUT_API)
    else:
        print("📝 Login failed \n")


    return courses
