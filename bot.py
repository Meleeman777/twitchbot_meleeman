import os
import json
import threading
import requests
import tokens 
from datetime import date


twitchclient_id=os.environ('TWITCHCLIENT')
twitchsecret=os.environ('TWITCHSECRET')
userStream=os.environ('USERSTREAM')
bot_token=os.environ('BOT_TOKEN')
bot_chatID_deutsch=os.environ('BOT_CHAT_ID_DEUTSCH')
bot_chatID_meleeman=os.environ('BOT_CHAT_ID_MELEEMAN')
bot_chatID_meleerama=os.environ('BOT_CHAT_ID_MELEERAMA')
#twitchclient_id=tokens.twitchclient_id
#twitchsecret=tokens.twitchsecret
#userStream=tokens.userStream
#bot_token=tokens.bot_token
#bot_chatID_deutsch=tokens.bot_chatID_deutsch
#bot_chatID_meleeman=tokens.bot_chatID_meleeman
#bot_chatID_meleerama=tokens.bot_chatID_meleerama

def is_TwitchOnline():
    try:
        
        tokenurl = 'https://id.twitch.tv/oauth2/token?client_id=' + twitchclient_id + \
                   '&client_secret=' + twitchsecret+'&grant_type=client_credentials'


        response = requests.post(tokenurl)
        response.raise_for_status()
        OAuth_Token = response.json()["access_token"]

        # Connection to Twitch
        response = requests.get('https://api.twitch.tv/helix/streams?user_login=' + \
                   userStream, headers={'Authorization': 'Bearer ' + \
                   OAuth_Token,'Client-Id': twitchclient_id})
        var=json.loads(response.content)


        # Dummy variable stored in text file for status update
        cwd = os.getcwd()
        filename= cwd + '/StreamTwitch_01Bot.txt'
        if (os.path.exists(filename) == False):
            f = open(filename, "w")
            f.write("FALSE")
            f.close()
        else:
            print("File Exists")    

        f = open(filename)
        boolean_online = f.read()
        f.close()

        # Twitch var data returns wether the stream just went live
        if var['data'] and boolean_online.upper()=='FALSE':
            message='Stream of : ['+str(userStream)+'](https://www.twitch.tv/'+str(userStream)+') is online. \n'


            telegram_bot_sendtext(message)
            f = open(filename, "w")
            f.write("TRUE")
            f.close()

        # Twitch var data returns wether the stream just went off-line    
        if not var['data'] and boolean_online.upper()=='TRUE':
            telegram_bot_sendtext('meleeman777'+' is offline')
            f = open(filename, "w")
            f.write("FALSE")
            f.close()
    
    except Exception as e: 
        print(e)
    
    return "Done"
    
# 3. Function that sends a notification to telegram when stream is on/off-line
def telegram_bot_sendtext(bot_message):
   
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + \
              bot_chatID_meleeman + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()


# 4 Running a check every 30seconds to see whether the Twitch stream is online
def main():
    timertime=30
    is_TwitchOnline()
   
    # 30sec timer
    threading.Timer(timertime, main).start()

# Run the main function
if __name__ == "__main__":
    main()