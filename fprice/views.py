#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from models import Trade, TradeForm, Shop, Goods, GClass, GSection
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.core.paginator import Paginator, InvalidPage, EmptyPage

import simplejson
from urllib import unquote
import datetime


def trade_last_list(request):
    goods_top = Trade.objects.values('goods__id','goods__title').annotate(goods_count=Count('goods')).order_by('-goods_count')[:10]
    trade_list = Trade.objects.order_by('-time')#[:10]

    paginator = Paginator(trade_list, 25)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        trades = paginator.page(page)
    except (EmptyPage, InvalidPage):
        trades = paginator.page(paginator.num_pages)

    return render_to_response('trade_last.html',
        {'trade_list': trades, 'goods_top': goods_top},
        context_instance=RequestContext(request))


def profile(request):
    goods_top = Trade.objects.values('goods__id','goods__title').annotate(goods_count=Count('goods')).order_by('-goods_count')[:10]

    sum7 = Trade.objects.filter(user=request.user).filter(spytrade=False).filter(time__gte=datetime.datetime.now()-datetime.timedelta(days=7)).aggregate(Sum('cost'))
    sum30 = Trade.objects.filter(user=request.user).filter(spytrade=False).filter(time__gte=datetime.datetime.now()-datetime.timedelta(days=30)).aggregate(Sum('cost'))

    trade_list = Trade.objects.filter(user=request.user).order_by('-time')#[:10]

    paginator = Paginator(trade_list, 25)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        trades = paginator.page(page)
    except (EmptyPage, InvalidPage):
        trades = paginator.page(paginator.num_pages)

    return render_to_response('trade_last.html',
        {'trade_list': trades, 'goods_top': goods_top, 'sum7': sum7, 'sum30': sum30},
        context_instance=RequestContext(request))


def trade_goods_list(request, goods_id):
    goods_top = Trade.objects.values('goods__id','goods__title').annotate(goods_count=Count('goods')).order_by('-goods_count')[:10]
    goods1 = Goods.objects.get(pk=goods_id)
    trade_list = Trade.objects.filter(goods=goods1).order_by('-time')
    #goods_list = Trade.objects.order_by('-time')#[:10]

    paginator = Paginator(trade_list, 25)
    # Make sure page request is an int. If not, deliver first page.
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    # If page request (9999) is out of range, deliver last page of results.
    try:
        trades = paginator.page(page)
    except (EmptyPage, InvalidPage):
        trades = paginator.page(paginator.num_pages)

    return render_to_response('trade_last.html',
        {'goods1': goods1, 'trade_list': trades, 'goods_top': goods_top},
        context_instance=RequestContext(request))


@login_required
def trade_add(request):
    goods_top = Trade.objects.values('goods__id','goods__title').annotate(goods_count=Count('goods')).order_by('-goods_count')[:10]

    price1 = 0
    results = []
    if request.method == 'POST': # If the form has been submitted...
        form = TradeForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            #return HttpResponseRedirect('/thanks/') # Redirect after POST

            #results = GClass.objects.filter(title__icontains=form.cleaned_data['goodstitle'])

            isOldTrade = False
            if int(form.cleaned_data["trade_pk"]) > 0:
                isOldTrade = True

            shop1 = None
            if int(form.cleaned_data["shop_pk"]) > 0:
                shop1 = Shop.objects.get(pk=form.cleaned_data["shop_pk"])
            else:
                shop1 = Shop(title=form.cleaned_data["shop"], type='mag')
                shop1.save()

            #gclass1 = None
            #if int(form.cleaned_data["gclass_pk"]) > 0:
            #    gclass1 = GClass.objects.get(pk=form.cleaned_data["gclass_pk"])
            #else:
            #    gclass1 = GClass(title=form.cleaned_data["gclass"], section=GSection.objects.get(pk=1)) #TODO GSection
            #    gclass1.save()

            goods1 = None
            if int(form.cleaned_data["gtitle_pk"]) > 0:
                goods1 = Goods.objects.get(pk=form.cleaned_data["gtitle_pk"])
                goods1.title = form.cleaned_data["gtitle"]
                goods1.ed = form.cleaned_data["ed"]
                #goods1.gclass = gclass1
                goods1.save()
            else:
                goods1 = Goods(title=form.cleaned_data["gtitle"], ed=form.cleaned_data["ed"])
                goods1.save()

            price1 = "%.2f" % ( float(form.cleaned_data['cost']) / float(form.cleaned_data['amount']) )

            if isOldTrade:
                trade1 = Trade.objects.get(pk=form.cleaned_data["trade_pk"])
            else:
                trade1 = Trade()

            trade1.user = request.user
            trade1.shop = shop1
            trade1.goods = goods1
            trade1.time = form.cleaned_data["time"]
            trade1.amount = form.cleaned_data["amount"]
            trade1.price = price1
            trade1.cost = form.cleaned_data["cost"]
            trade1.currency = form.cleaned_data["currency"]
            trade1.spytrade = form.cleaned_data["spytrade"]

            trade1.save()

            return HttpResponseRedirect("/")

    else:
        data = {'time': datetime.datetime.now, 'trade_pk': '0', 'shop_pk': '0', 'gclass_pk': '0', 'gtitle_pk': '0' }
        form = TradeForm(initial=data) # An unbound form

    return render_to_response('trade_add.html',
        {'price': price1, 'results': results, 'form': form, 'goods_top': goods_top},
        context_instance=RequestContext(request))


def trade_view(request, trade_id):
    trade = Trade.objects.get(pk=trade_id)

    data = {'trade_pk': trade_id, 'time': trade.time,
            'shop_pk': trade.shop.id, 'shop': trade.shop, 
            'gtitle_pk': trade.goods.id, 'gtitle': trade.goods.title, 'ed': trade.goods.ed,
            'amount': trade.amount, 'price': trade.price, 'cost': trade.cost,
            'currency': trade.currency, 'spytrade': trade.spytrade,
    }

    form = TradeForm(data)

    return render_to_response('trade_add.html',
        {'form': form}, context_instance=RequestContext(request))


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

    return render_to_response('shop_info.html',
        {'shop': shop, 'lat_y': lat_y, 'lon_x': lon_x, 'zoom': zoom, 'location': location},
        context_instance=RequestContext(request))


def shop_title_lookup(request):
    results = []
    if request.method == "GET":
        if request.GET.has_key(u'q'):
            value = request.GET[u'q']
            # Ignore queries shorter than length 2
            if len(value) > 1:
                model_results = Shop.objects.filter(title__icontains=value)
                results = [ (x.__unicode__(), x.id) for x in model_results ]
    json = simplejson.dumps(results)

    return HttpResponse(json, mimetype='application/json')


def gclass_title_lookup(request):
    results = []
    if request.method == "GET":
        if request.GET.has_key(u'q'):
            value = request.GET[u'q']
            # Ignore queries shorter than length 2
            if len(value) > 1:
                model_results = GClass.objects.filter(title__icontains=value)
                results = [ (x.__unicode__(), x.id) for x in model_results ]
    json = simplejson.dumps(results)

    return HttpResponse(json, mimetype='application/json')


def goods_title_lookup(request):
    results = []
    if request.method == "GET":
        if request.GET.has_key(u'q'):
            value = request.GET[u'q']
            # Ignore queries shorter than length 2
            if len(value) > 1:
                model_results = Goods.objects.filter(title__icontains=value)
                results = [ (x.__unicode__(), x.id) for x in model_results ]
    json = simplejson.dumps(results)

    return HttpResponse(json, mimetype='application/json')
