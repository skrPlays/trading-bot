from kiteconnect import KiteConnect
import requests

api_key = "1pb2l0oc8cnx45l7"
api_secret = "tzvlq8pvg58z97qzz8k5f5iqwo59nfo7"
kite = KiteConnect(api_key)
myuserID = 'YJ5684'
myPW = '<>'
my2fa = '<>'

def authenticate():
    # Obtaining Access Token
    login = requests.get(kite.login_url())
    cookies = ';'.join(['%s=%s'%(k,v) for k, v in login.history[1].cookies.items()])
    headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0',
            "X-Kite-Userid": myuserID, 'X-Kite-Version': '2.4.0',
            'Cookie': cookies, 'Referer': login.url
        }
    data = requests.post("https://kite.zerodha.com/api/login",{'user_id':myuserID,'password':myPW},headers=headers)
    data = requests.post("https://kite.zerodha.com/api/twofa",{'user_id':myuserID,'request_id':data.json()['data']['request_id'],'twofa_value':my2fa},headers=headers)

    public_token = data.cookies.get_dict()['public_token']
    user_id='user_id=' + myuserID
    headers.update({'Cookie': cookies+';'+'public_token='+public_token+';'+user_id})
    data = requests.get(login.url+'&skip_session=true', headers=headers)
    request_token = data.url.split("request_token")[1].split("=")[1]
    if  "&" in request_token:
        request_token = request_token.split("&")[0]

    data = kite.generate_session(request_token, api_secret)
    access_token = data['access_token']
    kite.set_access_token(access_token)
    print("Access Token: ",access_token)
    return kite, access_token