#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect

from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum

import simplejson
import datetime, time

from price.models import Trade, TradeForm, Goods, Section
from shop.models import Shop


def trade_list(request):
    trade_lists = Trade.objects.all()
    return object_list(request, queryset=trade_lists, paginate_by=25)


def trade_by_goods(request, goods_id):
    trade_list = Trade.objects.filter(goods__id=goods_id)
    return object_list(request, queryset=trade_list, paginate_by=25, extra_context={'goods1':Goods.objects.get(id=goods_id)})


@login_required
def trade_by_user(request):
    trade_list = Trade.objects.filter(user=request.user)
    return object_list(request, queryset=trade_list, paginate_by=25, extra_context={'is_profile':True})


@login_required
def trade_by_user_month(request, year, month):
    # Convert date to numeric format
    date = datetime.date(*time.strptime('%s-%s' % (year, month), '%Y-%b')[:3])
    trade_list = Trade.objects.filter(user=request.user, time__year=date.year, time__month=date.month).order_by('-time')
    # trade_month = Trade.objects.filter(user=request.user).dates('time','month')
    return object_list(request, queryset=trade_list, paginate_by=25, extra_context={'is_profile_month':True})


def search(request):
    query = request.GET.get('q', '')
    if query:
        results = Goods.objects.filter(title__icontains=query).distinct()
    else:
        results = []
    return object_list(request, queryset=results, paginate_by=25)


@login_required
def trade_add(request):
    price1 = 0
    results = []
    if request.method == 'POST': # If the form has been submitted...
        form = TradeForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data

            isOldTrade = False
            if int(form.cleaned_data["trade_pk"]) > 0:
                isOldTrade = True

            shop1 = None
            if int(form.cleaned_data["shop_pk"]) > 0:
                shop1 = Shop.objects.get(pk=form.cleaned_data["shop_pk"])
            else:
                shop1 = Shop(title=form.cleaned_data["shop"], type='mag')
                shop1.save()

            goods1 = None
            if int(form.cleaned_data["gtitle_pk"]) > 0:
                goods1 = Goods.objects.get(pk=form.cleaned_data["gtitle_pk"])
                goods1.title = form.cleaned_data["gtitle"]
                goods1.ed = form.cleaned_data["ed"]
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

            return HttpResponseRedirect("/") #('/thanks/')  # Redirect after POST

    else:
        data = {'time': datetime.datetime.now, 'trade_pk': '0', 'shop_pk': '0', 'gtitle_pk': '0' }
        form = TradeForm(initial=data) # An unbound form

    return render_to_response('price/trade_add.html',
        {'price': price1, 'results': results, 'form': form},
        context_instance=RequestContext(request))


@login_required
def trade_view(request, trade_id):
    trade = Trade.objects.get(pk=trade_id)

    data = {'trade_pk': trade_id, 'time': trade.time,
            'shop_pk': trade.shop.id, 'shop': trade.shop, 
            'gtitle_pk': trade.goods.id, 'gtitle': trade.goods.title, 'ed': trade.goods.ed,
            'amount': trade.amount, 'price': trade.price, 'cost': trade.cost,
            'currency': trade.currency, 'spytrade': trade.spytrade,
    }

    form = TradeForm(data)

    return render_to_response('price/trade_add.html',
        {'form': form}, context_instance=RequestContext(request))


def lookup(request, what):
    results = []
    if request.method == "GET":
        if request.GET.has_key(u'q'):
            value = request.GET[u'q']
            # Ignore queries shorter than length 2
            if len(value) > 1:
                if what == 'shop':
                    model_results = Shop.objects.filter(title__icontains=value)
                elif what == 'goods':
                    model_results = Goods.objects.filter(title__icontains=value)
                results = [ (x.__unicode__(), x.id) for x in model_results ]
    json = simplejson.dumps(results)

    return HttpResponse(json, mimetype='application/json')


@login_required
def edit_goods(request):
    value = ''
    if request.user.is_staff and request.method == "POST":
        if request.POST.has_key(u'value') and request.POST.has_key(u'id'):
            value = request.POST[u'value']
            goods_id = request.POST[u'id']
            goods1 = Goods.objects.get(id=goods_id)
            goods1.title = value
            goods1.save()
    return HttpResponse(value)
