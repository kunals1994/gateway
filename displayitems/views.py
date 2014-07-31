from django.shortcuts import render
from django.http import HttpResponse

from displayitems.models import Item

import urllib2
import json
from django_project import settings

BASE_DIR = settings.BASE_DIR

def home(request):
    return HttpResponse(open(BASE_DIR + "/assets/index.html", 'rb').read())

def swipe(request):
    return HttpResponse(open(BASE_DIR + "/assets/list.html", 'rb').read())

def rec_html(request):
    g = 3

    if(request.method=='GET'):
        g = request.GET.__getitem__("gender")
    else:
        g = request.POST.__getitem__("gender")

    ret = """<div id="itemdisplay" align="center" style="position:relative;">
                <br>
                <h3 class="brand-heading">
                    %(title)s
                </h3>
                <br>
                <img width=280 height=280 src="%(imgurl)s"/>
                <br>
                <p class="intro-text">
                    %(price)s
                </p>
                <br>
                <button class="btn btn-default btn-lg" onclick="javascript:void dislike();">
                    Dislike
                </button>
                &nbsp;
                <button id="buybutton" class="btn btn-default btn-lg" onclick="javascript:void buy('%(itemid)s');">
                    Buy!
                </button>
                &nbsp;
                <button class="btn btn-default btn-lg" onclick="javascript:void like();">
                    Like
                </button>
            </div>
            <br><br><br>"""
    ret = """<div class="itemdisplay" align="center"><br><h3 class="brand-heading">%(title)s</h3><br><img width=280 height=280 src="%(imgurl)s"/><br><p class="intro-text">%(price)s</p><br><a href=""><button class="btn btn-default btn-lg">Like</button></a>&nbsp;<a align="center" href="" class="btn btn-default btn-lg" id = "guest" onclick="javascript:void window.open('http://offer.ebay.com/ws/eBayISAPI.dll?BinConfirm&item=%(itemid)s','','width=1000, height=750');">Buy!</a>&nbsp;<a href=""><button class="btn btn-default btn-lg">Dislike</button></a></div><br><br><br>"""
    x = 0

    try:
        x = Item.objects.filter(gender=g)[0]
    except:
        print "goodbye_world"
        return HttpResponse("")
    params = {}
    params["title"] = x.title
    params["imgurl"] = x.imgurl
    params["price"] = x.price
    params["itemid"] = x.itemid

    x.delete()

    print len(Item.objects.all())

    return HttpResponse(ret%params)

def get_recs(request):
    pars = ""
    if(request.method == 'GET'):
        pars = request.GET
    else:
        pars = request.POST

    gender = pars.__getitem__('gender')
    
    
    cat_id = ""

    if(gender == "1"):
        cat_id = "1059"
    else:
        cat_id = "15724"

    url = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByCategory&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=KunalSha-8956-4859-9dca-aca35167996c&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&categoryId=%s&outputSelector=PictureURLSuperSize&paginationInput.entriesPerPage=10000" % cat_id
    count = 0


    response_string = urllib2.urlopen(url).read()
    response_json = json.loads(response_string)
    result_array = response_json["findItemsByCategoryResponse"][0]["searchResult"][0]["item"]

    for result in result_array:
        seconds_left = result["sellingStatus"][0]["timeLeft"][0]
        seconds_left= seconds_left[1:-1]

        seconds = int(seconds_left[:seconds_left.find("DT")])
        seconds_left = seconds_left[seconds_left.find("DT") + 2:]

        seconds *= 24
        seconds += int(seconds_left[:seconds_left.find("H")])
        seconds_left = seconds_left[seconds_left.find("H") + 1:]

        seconds *= 60
        seconds += int(seconds_left[:seconds_left.find("M")])
        seconds_left = seconds_left[seconds_left.find("M") + 1:]

        seconds *=60
        seconds += int(seconds_left)

        if( seconds < 300):
            continue

        item_id = result["itemId"][0]
        titl = result["title"][0]
        pric = result["sellingStatus"][0]["currentPrice"][0]["__value__"] + " " + result["sellingStatus"][0]["currentPrice"][0]["@currencyId"]
        try:
            img_url = result["pictureURLSuperSize"][0]
        except:
            img_url = result["galleryURL"][0]


        if(len(Item.objects.filter(itemid=item_id)) != 0):
            continue

        i = Item(imgurl = img_url, itemid = item_id, title = titl, price = pric, gender=int(gender))
        i.save()
        count +=1
    resp = ""
    if(count >= 1):
        resp+="Success"
    else:
        resp+="Failure"

    return HttpResponse(resp)

