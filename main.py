from Bot import json,logging, GoogleMeetBot

if __name__ == "__main__":

    try:
        
        with open('config_file.json', 'r') as json_file:
            data = json.load(json_file)
        email_addr = data['email']
        psw = data['password']
        meet_url = data['google_meet_url']
        cam=  data['camera']
        mic =  data['microphone']
        Gmeet= GoogleMeetBot(meet_url)
        Gmeet.google_login(email_addr,psw)
        Gmeet.join_meeting(cam,mic)
    except Exception as e:
        logging.error('An error occurred:', str(e))
