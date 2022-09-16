import requests
import unicodedata

def act(code, email, instant = False, sum = 30):
    act_url = 'https://bitobmen.pro/api/code-buy/'
    act_obj = {
        "code":f"{code}",
        "email":f"{email}",
        "indtsnt":f"{instant}"
    }
    '''
    sum_url = 'https://bitobmen.pro/api/code-sum/'
    sum_obj = {
        "code":f"{code}"
    }'''
    r = requests.post(act_url, json= act_obj)
    #l = requests.post(sum_url, json= sum_obj)
    #print(l.text)
    if r == "<Response [200]>":
        return f'код:{code} сумма '
    else:
        return False



print(act("grweghtre", "maxneb2507@gmail.com"))
