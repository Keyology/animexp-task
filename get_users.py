from pymongo import MongoClient
import pymongo
import pprint as pp
import random
import requests



db = client['animexp']




def get_users_account():
    users = db['users']
    user_account_info = {}
    try:
        for user in users.find():
            userID = user["userId"].strip()
            # pp.pprint(user)
            if (user['userEmail'] == "@gmail.com" or user['userEmail'] == None):
                continue
            else:
                url = f"https://animexp-backend.herokuapp.com/{userID}/lists"
                r = requests.get(url)
                response = r.json()
            if(response['firstName'] == None):
                continue
            else:
                pp.pprint(response['firstName'])
                pp.pprint(response['phoneNumber'])
                #pp.pprint(response['userAnimeList'])
                random_anime = response['userAnimeList'][0]['animeList']
                # print("***RANDOM ANIME***", random_anime)
                random_index = random.choice(range(len(random_anime)))
                # print("***RANDOM_INDEX***", random_anime)
                random_anime_2 = response['userAnimeList'][0]['animeList'][random_index][0]
                # print('**ANIME**',random_anime_2)
                user_name = response['firstName']
                userID = response['userId']
                # print("***USER NAME****", user_name)
                user_account_info[user_name] = [userID, response['phoneNumber'],random_anime_2]
                # print("***DICT ****", user_account_info)
        return user_account_info

    except Exception as error:
        print("ERROR GETTING USER", error)

def save_new_list():
    pass



if __name__ == "__main__":
    result = get_users_account()
    print(result)






