import requests
import pprint as pp
import userInfo
from celery import Celery
from datetime import date


app = Celery('tasks', backend='rpc://', broker='pyamqp://')

# @app.task
# def send_sms_recommendations():
#     """
#     import twillio api to send sms messages
#     call this endpoint to get recommendations for user localhost:8802/user/new/list save recs
#     send first 5 recommendations to user include title and poster image and link to view the rest

#     """
    
#     try:
#         users_info = userInfo.get_users_account()
#         for key, value in users_info.items():
#             print("KEY", key)
#             print("VAlue", value)
#         # url = "https://animexp-backend.herokuapp.com/user/new/list"
#         # r = requests.post(url)
#     except Exception as error:
#         print("ERROR RUNNING TASK:", error)

@app.task
def send_sms_recommendations():
    try:
        users_info = userInfo.get_users_account()
        today = date.today()
        anime_titles = []
        for _, value in users_info.items():
            user_new_list= {"userID": value[0],"name":f"sms recommendations {today}","description":f"{today} sms recommendations", "list":[value[2]]}
            create_new_list = requests.post("http://localhost:8002/user/new/list", data=user_new_list)
            if(create_new_list.status_code != 200):
                print('STATUS CODE FOR CREATE NEW LIST',create_new_list.status_code)
                continue
            response = create_new_list.json()
            user_anime_recommendations = response['animeRecommendations'][0:4]
        for i in range(len(user_anime_recommendations)):
            url = f"https://animexp-backend.herokuapp.com/search/anime/{user_anime_recommendations[i][0]}"
            print("url", url)
            request = requests.get(url)
            resp = request.json()
            anime_titles.append(resp[0]["animeTitles"][0])
        wake_up_server = request.get("https://sms-server-1.herokuapp.com/")


        
    except Exception as error:
        print("Error sending sms recomendations", error)



if __name__ == "__main__":
    result = send_sms_recommendations()






    #loop over dict
    #get the key and value
    #get the userID and animeID and send it over to the create new list endpoint
    #get a list of anime recomendations back and and get the first 5 in the json array
    #parse the json and get the title & image 