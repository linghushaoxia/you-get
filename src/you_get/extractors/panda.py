#!/usr/bin/env python

__all__ = ['panda_download']

import json
import time

from common import *


def panda_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    roomid = url[url.rfind('/')+1:]
    json_request_url ="http://www.panda.tv/api_room_v2?roomid={}&__plat=pc_web&_={}".format(roomid, int(time.time()))
    content = get_html(json_request_url)
    api_json = json.loads(content)
    
    errno = api_json["errno"]
    errmsg = api_json["errmsg"]
    if errno:
        raise ValueError("Errno : {}, Errmsg : {}".format(errno, errmsg))
    data = api_json["data"]
    title = data["roominfo"]["name"]
    room_key = data["videoinfo"]["room_key"]
    plflag = data["videoinfo"]["plflag"].split("_")
    status = data["videoinfo"]["status"]
    if status is not "2":
        raise ValueError("The live stream is not online! (status:%s)" % status)

    data2 = json.loads(data["videoinfo"]["plflag_list"])
    rid = data2["auth"]["rid"]
    sign = data2["auth"]["sign"]
    ts = data2["auth"]["time"]
    real_url = "http://pl{}.live.panda.tv/live_panda/{}.flv?sign={}&ts={}&rid={}".format(plflag[1], room_key, sign, ts, rid)
    
    print_info(site_info, title, 'flv', float('inf'))
    if not info_only:
        download_urls([real_url], title, 'flv', None, output_dir, merge = merge)

site_info = "panda.tv"
download = panda_download
download_playlist = playlist_not_supported('panda')
