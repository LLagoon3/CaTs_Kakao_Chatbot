from django.shortcuts import render
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://test-project-d1903-default-rtdb.firebaseio.com/' 
})
ref = db.reference() 
ref.update({'data2' : {'id': 3}}) 

ref = db.reference('data1')
print(ref.get())
