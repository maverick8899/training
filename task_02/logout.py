import config


def execute(session, headers, cookies, api):

    print('📝 headers:', headers)
    print('📝 cookies:', cookies)

    response = session.get(api, cookies=cookies, headers=headers)
    response = session.get(api, cookies=cookies, headers=headers)
    # print(response.text)

    if response.status_code == 200 or 302:
        print("✅✅✅ Logout successfully ✅✅✅ \n")
    else:
        print("📝 Logout failed \n")
