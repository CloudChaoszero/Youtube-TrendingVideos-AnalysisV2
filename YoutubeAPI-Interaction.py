import requests
import json

import os 
import sys
sys.path.insert(0,os.path.join("Resources"))

from config import api_key




regionCode_list = ["at","the","that","ch","cn","from","dk","is","be","fr","is",
                   "mx","us","kr","nl","nz","jp","ru","vn","for"]

urlRequest_regionCodeList_forVideoIDs = [f"https://www.googleapis.com/youtube/v3/videos?part=statistics&chart=mostPopular&regionCode={regCode.upper()}&maxResults=25&key="+ api_key for regCode in regionCode_list]

#Get Video Ids
urlRequest_forVideoIds = "https://www.googleapis.com/youtube/v3/videos?part=statistics&chart=mostPopular&regionCode=US&maxResults=25&key="+api_key

def getAPIResponse(url_string):
    try:
        resp= requests.get(url_string)
        return([resp,resp.json()])
    except:
        print("Error from request. Check URL link or ensure have correct API key")

def getVideoIds(response_object):
    response = response_object[1]
    listOf_trendingVideo_ids = [i["id"] for i in response["items"]]
    return(listOf_trendingVideo_ids)

response_videoIDs_perRegCode = [getAPIResponse(urlReq) for urlReq in urlRequest_regionCodeList_forVideoIDs]
trendingVideosList_perRegCode = [getVideoIds(response_video) for response_video in response_videoIDs_perRegCode]

response_videoIDs = getAPIResponse(urlRequest_forVideoIds)
trendingVideosList_YT = getVideoIds(response_videoIDs)

print(trendingVideosList_YT)
print(trendingVideosList_perRegCode)

# Get Video Stats

#// TODO: Take out following line if code works
# url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={api_key}&part=snippet,statistics"

def acquireVideoInformation(videoID_list, apiKey, printout=None):
    video_stats_dict = {"Title":[],"PublishedAt":[],"ChannelID":[],"Description":[],"ChannelTitle":[],"CategoryId":[],\
              "ViewCount":[],"LikeCount":[],"DislikeCount":[],"FavoriteCount":[],"CommentCount":[]}
    for video_id in videoID_list:
        ressponse_videoInfo = requests.get(f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&key={apiKey}&part=snippet,statistics").json()
        rest2_in = ressponse_videoInfo["items"][0]

        video_stats_dict["Title"].append(rest2_in["snippet"]["title"])
        video_stats_dict["PublishedAt"].append(rest2_in["snippet"]["publishedAt"])
        video_stats_dict["ChannelID"].append(rest2_in["snippet"]["channelId"])
        video_stats_dict["Description"].append(rest2_in["snippet"]["description"])
        video_stats_dict["ChannelTitle"].append(rest2_in["snippet"]["channelTitle"])
        video_stats_dict["CategoryId"].append(rest2_in["snippet"]["categoryId"])
        video_stats_dict["ViewCount"].append(rest2_in["statistics"]["viewCount"])
        video_stats_dict["LikeCount"].append(rest2_in["statistics"]["likeCount"])
        video_stats_dict["DislikeCount"].append(rest2_in["statistics"]["dislikeCount"])
        video_stats_dict["FavoriteCount"].append(rest2_in["statistics"]["favoriteCount"])
        video_stats_dict["CommentCount"].append(rest2_in["statistics"]["commentCount"])
    if printout is True:
        print(video_stats_dict)
    else: 
        pass
    return(video_stats_dict)

vidStats = acquireVideoInformation(trendingVideosList_YT, api_key, printout=True)


#-----------------------------------------------------
'''
Output Dataframe to json
'''
from datetime import datetime
from pandas import DataFrame

now = datetime.now()
year = str(now.year)
month = str(now.month)
day = str(now.day)


def outputToDataFrame(information):
    '''
    Requirement: Input DataFrame object from pandas library
    '''
    return(DataFrame(information))

vidStats_df= outputToDataFrame(vidStats)
vidStats_df.to_csv(f"Data/YoutubeVideoStats-{month}{day}{year}.csv")


print(json.dumps(video_stats, indent=4, sort_keys=False))



#Plan out rest of code


## Do a sql alchemy version. ONce that is complete, then 