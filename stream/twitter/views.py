from django.shortcuts import render
import time
from django.http import HttpResponse
import pymongo
from pymongo import MongoClient
import json
#from __future__ import print_function
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

f_tweets=None
fl_tweet=[]


ckey = 'SndBbMk3D5y0n0fp5rOtVHkxN'
csecret='7C4iAqTVnrNWR5TCtc31Llaaab9jWjibJ8aaD7ttTynFhHbhXX'
atoken='963706973077278720-GsvRR95JQCM96lYHEkZAGk0CftsV4Ut'
asecret='YruNcrziBU7A5GoNwln5culM3KX3CscHsfpeagH3ilgTO'

MONGO_HOST= 'mongodb://localhost/twitterdb'

client= MongoClient(MONGO_HOST)
db=client.twitterdb

class listener(StreamListener):
    def __init__(self):
        self.num=0


    def on_data(self, data,num=0):

        self.num+=1
        print (data)
        print("______________________________________________________________________",self.num)



        datajson=json.loads(data)
        db.twitter_search.insert(datajson)

        if(self.num<50):
            return True
        else:
            return False

    def on_error(self, status):
        print (status)


auth=OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

def search(request):

    return render(request,'twitter/filter.html')



def index(request):
    #print(type(twitterStream))
    if request.method == 'POST':
        twitterStream=Stream(auth, listener())
        x=request.POST.get('name_field','')
        twitterStream.filter(track=[x])
    return render(request,'twitter/index.html')


def filter(request):
    global f_tweets, all_tweets ,fl_tweet,users,solution
    coll=db.twitter_search

    if request.method == 'POST':
        fl_tweet=[]




        word=request.POST.get('name_field')
        position=request.POST.get('order','middle')

        ct=request.POST.get('follower_count',0)

        order1=request.POST.get('tw_num','greater than')
        rt=request.POST.get('retweet_count',0)
        order2=request.POST.get('rw_num','egual to')
        ft=request.POST.get('favourites_count',0)
        order3=request.POST.get('fw_num','greater than')

        lang=request.POST.get('lang')

        s_date=request.POST.get('s_dat')
        e_date=request.POST.get('e_dat')

        strt_date=time.strptime(s_date,"%Y-%m-%d")
        end_date=time.strptime(e_date,"%Y-%m-%d")
        ordering=request.POST.get('ord','Asc')

        cs=request.POST.get('csv',0)
        #print(cs)
        if(ordering=='Asc'):
            ord=1
        else:
            ord=-1

        #print(ord)

        if(position=="starts"):
            word='^' +word
        elif(position=="ends"):
            word=word + '$'


        if(order1=="greater than"):
            comp1="$gt"
        elif(order1=="less than"):
            comp1="$lt"
        else:
            comp1="$eq"

        if(order2=="greater than"):
            comp2="$gt"
        elif(order2=="less than"):
            comp2="$lt"
        else:
            comp2="$eq"

        if(order3=="greater than"):
            comp3="$gt"
        elif(order3=="less than"):
            comp3="$lt"
        else:
            comp3="$eq"





        f_tweets = coll.find(
            {
                "$and":
                    [
                        {'text':{'$regex':word}},
                        {'user.followers_count':{comp1: int(ct)}},
                        {'retweet_count':{comp2 : int(rt)}},
                        {'user.favourites_count':{comp3:int(ft)}},
                        {'lang':lang},
                    ]
                },{'text':1,'_id':0,'reply_count':1,'user.followers_count':1,'retweet_count':1,'lang':1,'created_at':1,
                   'user.favourites_count':1,"timestamp_ms":1,"user.time_zone":1,'user.name':1}).sort("timestamp_ms",ord)



        for doc in f_tweets:
            date=doc['created_at']
            l_date=date.split(' ')
            t_date=time.strptime(l_date[1]+ ':'+ l_date[2]+':'+l_date[5],'%b:%d:%Y')
            if t_date>=strt_date and t_date<=end_date:
                fl_tweet.append(doc)


        saveFile = open('C:/Users/Likhita/Desktop/twitter.csv','a')
        saveFile.write( "Tweet_text" + "," + "Created_at" + ',' + "Retweet_count" + ',' + "favourites_count" + ',' +'Time_zone'
                            ',' + "Followers_count" )

        saveFile.write("\n")


        if(cs=='1'):
            for tweet in fl_tweet:
                try:
                    saveFile = open('C:/Users/Likhita/Desktop/twitter.csv','a')
                    t=tweet['text']
                    t_new=t.replace('\"','\"\"')
                    saveFile.write(
                                  "\"" + t_new + "\"" + ',' +
                                  tweet['created_at'] + ',' + str(tweet['retweet_count']) + ',' +
                                  str(tweet['user']['favourites_count']) + ',' + str(tweet['user']['time_zone'])+
                                  ',' + str(tweet['user']['followers_count'])
                    )
                    saveFile.write("\n")
                    saveFile.close()

                except:
                     saveFile = open('C:/Users/Likhita/Desktop/twitter.csv','a')
                     saveFile.write('ERROR : Couldn\'t import tweet because of some special characters contained within!')
                     saveFile.write("\n")
                     saveFile.close()



        paginator=Paginator(fl_tweet,6)
        users = paginator.get_page(1)

        solution=[[],[]]
        for user in users:
            solution[0].append(user['text'])
            solution[1].append(user['created_at'])



    else:

        page= request.GET.get('page',1)
        paginator=Paginator(fl_tweet,6)
        users = paginator.get_page(page)
        solution=[[],[]]
        for user in users:
            solution[0].append(user['text'])
            solution[1].append(user['created_at'])



    context={'tweets':solution[0],'created_at':solution[1],'users':users}
    return render(request,'twitter/name.html',context)

