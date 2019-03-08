import requests
import json

import os
import sys
sys.path.insert(0, os.path.join("Resources"))

#API Congfiguration Key
from config import api_key

#Get Regions for their respective Trending Video List
regionCode_list = ["at", "ch", "cn", "dk", "is", "be", "fr", "is",
                   "mx", "us", "kr", "nl", "nz", "jp", "ru", "vn"]

# Get Trending Video Ids for each Region Code
urlRequest_regionCodeList_forVideoIDs = [
        "https://www.googleapis.com/youtube/v3/videos?part=statistics&" + 
        f"chart=mostPopular&regionCode={regCode.upper()}&maxResults=25&key=" 
        + api_key for regCode in regionCode_list]

#API Call.
def getAPIResponse(url_string):
    try:
        resp = requests.get(url_string)
        return([resp, resp.json()])
    except:
        print("Request Error. Check URL link or ensure have correct API key")


#From Response object, get each video's ID.
def getVideoIds(response_object):
    response = response_object[1]
    listOf_trendingVideo_ids = [i["id"] for i in response["items"]]
    return(listOf_trendingVideo_ids)

#Obtain Each Video's Statistics and Information.
def acquireVideoInformation(videoID_list, apiKey, printout=None):
    video_stats_dict = {"VideoID": [], "Title": [], "PublishedAt": [], 
                        "ChannelID": [], "Description": [], "ChannelTitle": [],
                        "CategoryId": [], "ViewCount": [], "LikeCount": [], 
                        "DislikeCount": [], "FavoriteCount": [], "CommentCount": []}
    
    for video_id in videoID_list:

        #Youtube API call for statistics
        response_videoInfo = requests.get(
            f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&" + 
            f"key={apiKey}&part=snippet,statistics").json()
        rest2_in = response_videoInfo["items"][0]

        video_stats_dict["VideoID"].append(video_id)
        video_stats_dict["Title"].append(rest2_in["snippet"]["title"])
        video_stats_dict["PublishedAt"].append(
            rest2_in["snippet"]["publishedAt"])
        video_stats_dict["ChannelID"].append(rest2_in["snippet"]["channelId"])
        video_stats_dict["Description"].append(
            rest2_in["snippet"]["description"])
        video_stats_dict["ChannelTitle"].append(
            rest2_in["snippet"]["channelTitle"])
        video_stats_dict["CategoryId"].append(
            rest2_in["snippet"]["categoryId"])
        try:
            video_stats_dict["ViewCount"].append(
                rest2_in["statistics"]["viewCount"])
        except:
            video_stats_dict["ViewCount"].append(0)
        try:
            video_stats_dict["LikeCount"].append(
                rest2_in["statistics"]["likeCount"])
        except:
            video_stats_dict["LikeCount"].append(0)
        try:
            video_stats_dict["DislikeCount"].append(
                rest2_in["statistics"]["dislikeCount"])
        except:
            video_stats_dict["DislikeCount"].append(0)
        video_stats_dict["FavoriteCount"].append(
            rest2_in["statistics"]["favoriteCount"])
        try:
            video_stats_dict["CommentCount"].append(
                rest2_in["statistics"]["commentCount"])
        except:
            video_stats_dict["CommentCount"].append(0)
    if printout is True:
        print(video_stats_dict)
    else:
        pass
    return(video_stats_dict)


trendingVideos_information = {}
for i, response_video in enumerate(urlRequest_regionCodeList_forVideoIDs):
    # trendingVideo list
    capString = regionCode_list[i].upper()
    trendingVideos_information[capString] = [getAPIResponse(response_video)]
    # description of trending videos
    getVids = getVideoIds(trendingVideos_information[capString][0])
    trendingVideos_information[capString].append(getVids)
    trendingVideos_information[capString].append(acquireVideoInformation(
        trendingVideos_information[capString][1], api_key, printout=True))

# -----------------------------------------------------
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

#For each key and piece of information
for key, info in trendingVideos_information.items():
    vidStats_df = outputToDataFrame(info[2])
    vidStats_df["RegionCode"] = [key.upper()
                                 for i in range(vidStats_df.shape[0])]
    vidStats_df["Date"] = [
        f"{month}/{day}/{year}" for i in range(vidStats_df.shape[0])]
    vidStats_df.to_csv(f"Data/YoutubeVideoStats-{key}-{month}{day}{year}.csv")