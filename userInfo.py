import pymongo
import pprint as pp
import random
import requests
import os
from pymongo import MongoClient



def parse_dotenv():
    file_content = None
    with open(".env", 'rt') as f:
        file_content = f.read()
        file_content = file_content[1:-1]
    return file_content
    

db_url = parse_dotenv()
client = MongoClient(db_url)
db = client['animexp']




def get_users_account():
    """This function searches through the database to find users who have signeup
    and return a dictionary the has the user name as a key and a list that contains the userID, phonenumber, animeID"""
    users = db['users']
    try:
        user_account_info = {}
        for user in users.find():
            userID = user["userId"].strip() 
            if (user['userEmail'] == "@gmail.com" or user['userEmail'] == None):
                #if the user does not have an original email then skip them
                continue
            else:
                url =f'https://animexp-backend.herokuapp.com/user/{userID}/lists'
                r = requests.get(url)
                if(r.status_code != 200):
                    continue
                response = r.json()
                
                if('firstName' not in response or 'phoneNumber' not in response or response['firstName'] == None or carrier not in response):
                    """The firstName key and PhoneNumber key does not exist in all mongo docs if thats the case, skip it """
                    continue
                else:
                    for index in range(len(response['userAnimeList'])):
                        random_anime = response['userAnimeList'][index]["animeList"]
                        if ("sms recommendations" in response['userAnimeList'][index]["animeListName"]):
                            continue
                        #Get a random anime from the users list
                        random_index = random.choice(range(len(random_anime)))
                        random_anime_2 = response['userAnimeList'][index]['animeList'][random_index][0]
                        user_first_name = response['firstName']
                        userID = response['userId']
                        user_phoneNumber = response['phoneNumber']
                        user_carrier = response['carrier']
                        user_account_info[user_first_name] = [userID, user_phoneNumber,user_carrier,random_anime_2]
        return user_account_info

    except Exception as error:
        print("ERROR GETTING USER:", error)



if __name__ == "__main__":
    result = get_users_account()
    # print(result)
   






