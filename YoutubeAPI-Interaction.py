import os 
import sys

sys.path.insert(0,os.path.join("Resources"))
from config import api_key


#Get Video Ids
urlRequest_forVideoIds = "https://www.googleapis.com/youtube/v3/videos?part=statistics&chart=mostPopular&regionCode=US&maxResults=25&key="+api_key

def getAPIResponse(url_string):
    resp= requests.get(url_string)
    return([resp,resp.json()])

def getVideoIds(response_object):
    response = response_object[1]
    listOf_trendingVideo_ids = [i["id"] for i in response["items"]]
    return(listOf_trendingVideo_ids)
response_videoIDs = getAPIResponse(urlRequest_forVideoIds)
listt = getVideoIds(response_videoIDs)
print(listt)