import requests
from datetime import time
from datetime import datetime 
import urllib.request, urllib.parse , urllib.error
import json

API = "https://btuc27vrq7.execute-api.us-east-1.amazonaws.com/....."

class BotHandler:
    def __init__(self, token):
            self.token = token
            self.api_url = "https://api.telegram.org/bot{}/".format(token)

    #url = "https://api.telegram.org/bot<token>/"

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_first_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = None

        return last_update


token = 'xxxxxxx:xxxxxxxxxxxxxxxxxxxxxxx' #Token of your bot
magnito_bot = BotHandler(token) #Your bot's name



def main():
    new_offset = 0
    print('hi, now launching...')

    while True:
        all_updates=magnito_bot.get_updates(new_offset)

        if len(all_updates) > 0:
            for current_update in all_updates:
                print(current_update)
                first_update_id = current_update['update_id']
                if 'text' not in current_update['message']:
                    first_chat_text = 'New member'
                else:
                    first_chat_text = current_update['message']['text']
                    
                first_chat_id = current_update['message']['chat']['id']
                if 'first_name' in current_update['message']:
                    first_chat_name = current_update['message']['chat']['first_name']
                elif 'from' in current_update['message']:
                    first_chat_name = current_update['message']['from']['first_name']
                

                now = datetime.now()
                time = now.strftime("%I:%H:%S %p")
                tmp = time.split()[1]

                if first_chat_text == 'Hi' or first_chat_text == 'Hii' or first_chat_text == 'Hello' :
                    if tmp == 'AM':
                        magnito_bot.send_message(first_chat_id, 'Good Morning ' + first_chat_name)
                        new_offset = first_update_id + 1
                    else:
                        magnito_bot.send_message(first_chat_id, 'Good Evening ' + first_chat_name)
                        new_offset = first_update_id + 1
                
                else:
                    html = API + urllib.parse.urlencode({'command':first_chat_text})
                    data = urllib.request.urlopen(html).read()
                    ans = json.loads(data)
                    
                    magnito_bot.send_message(first_chat_id, ans)
                    new_offset = first_update_id + 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
