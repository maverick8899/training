import os

# EMAIL = "binhlan@gmail.com"
# PASSWORD = "toisethanhcong08092003"

# EMAIL = "trankimbang@gmail.com"
# PASSWORD = "toisethanhcong"

# EMAIL = "tmaverick8989@gmail.com"
# PASSWORD = "toisethanhcong08092003"

EMAIL = "2151050035bang@ou.edu.vn"
PASSWORD = "toisethanhcong08092003@"

# WEB_URL = "https://www.udemy.com/"
WEB_URL = "https://www.udemy.com/join/login-popup/?passwordredirect=True"
LOGIN_API="https://www.udemy.com/join/login-popup/?passwordredirect=True&response_type=json"
LOGOUT_API="https://www.udemy.com/user/logout"
GET_COURSE_API="https://www.udemy.com/api-2.0/users/me/subscribed-courses"
CSRF_TOKEN="wtKAnEBUTPvSkFLO2hktTY001gBFI4sv" 

def email():
    return os.getenv("EMAIL")

def password():
    return os.getenv("PASSWORD")