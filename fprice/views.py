#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext

from models import Trade, TradeForm, Shop, Goods, GClass
from django.contrib.auth.decorators import login_required

def trade_last_list(request):
    trade_list = Trade.objects.order_by('-time')#[:10]
    return render_to_response('trade_last.html', {'trade_list': trade_list}, context_instance=RequestContext(request))

@login_required
def trade_add(request):
    form = TradeForm()
    return render_to_response('trade_add.html', {'form': form}, context_instance=RequestContext(request))

def shop_info(request, shop_id):
    shop = Shop.objects.get(pk=shop_id)
    return render_to_response('shop_info.html', {'shop': shop}, context_instance=RequestContext(request))

def trade_goods_list(request, goods_id):
    gclass1 = GClass.objects.get(pk=goods_id)
    goods_list = Trade.objects.filter(goods__gclass=gclass1).order_by('-time')
    #goods_list = Trade.objects.order_by('-time')#[:10]
    return render_to_response('goods_last.html', {'goods_list': goods_list}, context_instance=RequestContext(request))
