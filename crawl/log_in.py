import requests


def log_in(username:str,password:str):
    

    res = requests.get('https://kscdirect.com/')
    cookies = res.cookies.get_dict()['ecomm_session_id']

    session = requests.Session()
    session.cookies.set('ecomm_session_id', cookies)
    
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'ecomm_session_id=bb2c88efbe2b1baac408e3eee384fc; _gcl_au=1.1.490205299.1716417240; _ga=GA1.1.1927894199.1716417240; _ga_CV13R17X3C=GS1.1.1716696260.2.1.1716697212.47.0.0',
        'Origin': 'https://kscdirect.com',
        'Referer': 'https://kscdirect.com/account_login.php',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    session.headers.update(headers)
    
    data = {
        'action': 'login',
        'return_to': '',
        'username': username,
        'password': password,
    }

    response = session.post('https://kscdirect.com/user_auth.php', data=data)
    if response.status_code == 200:
        print('200: login success.')
    return session
