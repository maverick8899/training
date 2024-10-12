def execute(session, headers, cookies, api):

    print('📝 headers:', headers)
    print('📝 cookies:', cookies)

    response = session.get(
        api,
        cookies=cookies,
        headers=headers,
    )
    if response.status_code == 200:
        print("✅✅✅ get courses successfully ✅✅✅ \n")
        print("📝 courses: ", response.json())
        return response.json()
    else:
        print("📝 get courses failed \n", response.json()) 
