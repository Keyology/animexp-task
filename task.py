from celery import Celery
from get_users import *
from twilio.rest import Client
import requests
import pprint as pp




app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def send_sms_recommendations():
    """
    import twillio api to send sms messages
    call this endpoint to get recommendations for user localhost:8802/user/new/list save recs
    send first 5 recommendations to user include title and poster image and link to view the rest

    """
    pass 
