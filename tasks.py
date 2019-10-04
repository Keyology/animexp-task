import requests
import pprint as pp
import userInfo
from datetime import date

def send_sms_recommendations():
    try:
        users_info = userInfo.get_users_account()
        pp.pprint(users_info)
        today = date.today()
        anime_titles = []
        for key, value in users_info.items():
            user_new_list= {"userID": value[0],"name":f"sms recommendations {today}","description":f"{today} sms recommendations", "list": [value[3]]}
            create_new_list = requests.post("https://animexp-backend.herokuapp.com/user/new/list", data=user_new_list)
            
            if(create_new_list.status_code != 200):
                print('STATUS CODE FOR CREATE NEW LIST',create_new_list.status_code)
                continue
            response = create_new_list.json()
            user_anime_recommendations = response['animeRecommendations'][0:4]
        for i in range(len(user_anime_recommendations)):
            url = f"https://animexp-backend.herokuapp.com/search/anime/{user_anime_recommendations[i][0]}"
            print("url", url)
            get_title = requests.get(url)
            resp = get_title.json()
            anime_titles.append(resp[0]["animeTitles"][0])
        wake_up_server = requests.get("https://flask-sms-server.herokuapp.com/")
        if(wake_up_server.status_code == 200):
            sms_data = {'username':key, 'phonenumber': value[1],
            'carrier': value[2], 'anime_recs_titiles':anime_titles}
            send_sms = requests.post('https://flask-sms-server.herokuapp.com/api/v1/send/sms', data=sms_data)
        else:
            print("ERROR SENDING REQUEST TO SMS")
    task_completed = 'DONE'
    return task_completed
        
        


        
    except Exception as error:
        print("Error sending sms recomendations", error)



if __name__ == "__main__":
    task = send_sms_recommendations()
    print(task)






    #loop over dict
    #get the key and value
    #get the userID and animeID and send it over to the create new list endpoint
    #get a list of anime recomendations back and and get the first 5 in the json array
    #parse the json and get the title & image 