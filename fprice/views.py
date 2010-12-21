#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse

from models import Trade, TradeForm, Shop, Goods, GClass
from django.contrib.auth.decorators import login_required

import simplejson
from urllib import unquote

def trade_last_list(request):
    trade_list = Trade.objects.order_by('-time')#[:10]
    return render_to_response('trade_last.html', {'trade_list': trade_list}, context_instance=RequestContext(request))

@login_required
def trade_add(request):

    price = 0
    results = []
    if request.method == 'POST': # If the form has been submitted...
        form = TradeForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            #return HttpResponseRedirect('/thanks/') # Redirect after POST
            results = GClass.objects.filter(title__icontains=form.cleaned_data['goodstitle'])
            price = unicode(float(form.cleaned_data['cost']) / float(form.cleaned_data['amount']))
    else:
        form = TradeForm() # An unbound form

    return render_to_response('trade_add.html', {'price': price, 'results': results, 'form': form}, context_instance=RequestContext(request))

def trade_view(request, trade_id):
    trade = Trade.objects.get(pk=trade_id)
    data = {'goodstitle': trade.goods.title,'ed': trade.goods.ed, 'amount': trade.amount, 'price': trade.price, 'gtype': trade.goods.gclass, 'shop': trade.shop, 'cost': unicode(float(trade.amount) * float(trade.price))}
    form = TradeForm(initial=data)

    return render_to_response('trade_add.html', {'form': form}, context_instance=RequestContext(request))

def shop_info(request, shop_id):
    shop = Shop.objects.get(pk=shop_id)
    return render_to_response('shop_info.html', {'shop': shop}, context_instance=RequestContext(request))

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

def trade_goods_list(request, goods_id):
    gclass1 = GClass.objects.get(pk=goods_id)
    goods_list = Trade.objects.filter(goods__gclass=gclass1).order_by('-time')
    #goods_list = Trade.objects.order_by('-time')#[:10]
    return render_to_response('goods_last.html', {'goods1': gclass1, 'goods_list': goods_list}, context_instance=RequestContext(request))
