#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from models import Trade, TradeForm, Shop, Goods, GClass, GSection
from django.contrib.auth.decorators import login_required
from django.db.models import Count

import simplejson
from urllib import unquote
import datetime


def trade_last_list(request):
    trade_list = Trade.objects.order_by('-time')#[:10]
    goods_top = Trade.objects.values('goods','goods__title').annotate(Count('goods')).order_by('-goods__count')[:10]

    return render_to_response('trade_last.html',
        {'trade_list': trade_list, 'goods_top': goods_top},
        context_instance=RequestContext(request))


def profile(request):
    trade_list = Trade.objects.filter(user=request.user).order_by('-time')#[:10]

    return render_to_response('trade_last.html',
        {'trade_list': trade_list},
        context_instance=RequestContext(request))


def trade_goods_list(request, goods_id):
    goods1 = Goods.objects.get(pk=goods_id)
    trade_list = Trade.objects.filter(goods=goods1).order_by('-time')
    #goods_list = Trade.objects.order_by('-time')#[:10]

    return render_to_response('trade_last.html',
        {'goods1': goods1, 'trade_list': trade_list},
        context_instance=RequestContext(request))


@login_required
def trade_add(request):

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
        {'price': price1, 'results': results, 'form': form},
        context_instance=RequestContext(request))


def trade_view(request, trade_id):
    trade = Trade.objects.get(pk=trade_id)
    data = {'trade_pk': trade_id, 'shop_pk': trade.shop.id, 'currency': trade.currency, 'time': trade.time, 'gtitle': trade.goods.title, 'gtitle_pk': trade.goods.id, 'ed': trade.goods.ed, 'amount': trade.amount, 'price': trade.price, 'shop': trade.shop, 'cost': trade.cost, 'spytrade': trade.spytrade }
    form = TradeForm(data)

    return render_to_response('trade_add.html',
        {'form': form}, context_instance=RequestContext(request))


def shop_info(request, shop_id):
    shop = Shop.objects.get(pk=shop_id)

    return render_to_response('shop_info.html',
        {'shop': shop}, context_instance=RequestContext(request))


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
