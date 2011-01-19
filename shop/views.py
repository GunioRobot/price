#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from shop.models import Shop

import httplib
import re
from xml.dom.minidom import parseString

def shop_info(request, shop_id):
    shop = Shop.objects.get(pk=shop_id)
    lon_x = 0
    lat_y = 0
    zoom = 12
    location = 0
    if not shop:
        shop = Shop.objects.get(pk=1)
    if shop.addr:
        if (not shop.addr.x or not shop.addr.y):
            ip = request.META['REMOTE_ADDR']

            # Посылка запроса на ipgeobase.ru
            conn = httplib.HTTPConnection("194.85.91.253:8090")
            conn.request("POST", "/geo/geo.html",\
                        "<ipquery><fields><all/></fields><ip-list><ip>" + ip +\
                        "</ip></ip-list></ipquery>")
            resp = conn.getresponse()

            data = resp.read()
            conn.close()

            # если ничего не найдено
            if re.search("<message>Not found</message>", data):
                location = 2 # адрес нулевой
            else:
                dom = parseString(data)
                # http://blog.ipgeobase.ru/?p=37 - теги расписаны тут
                lat_y = dom.documentElement.getElementsByTagName('lat')[0].firstChild.nodeValue
                lon_x = dom.documentElement.getElementsByTagName('lng')[0].firstChild.nodeValue
                location = 1 # есть адрес города
        else:
            lon_x = shop.addr.x
            lat_y = shop.addr.y
            zoom = 16
    else:
        location = 2

    return render_to_response('shop/shop_detail.html',
        {'shop': shop, 'lat_y': lat_y, 'lon_x': lon_x, 'zoom': zoom, 'location': location},
        context_instance=RequestContext(request))
