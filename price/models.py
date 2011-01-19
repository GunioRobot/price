#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django import forms
from shop.models import Shop


class Section(models.Model):
    title = models.CharField(max_length=50)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["title"]


ED_CHOICES = (
    ('sh', 'шт'),
    ('kg', 'кг'),
    ('l', 'л'),
    ('m', 'м'),
    ('gr', 'гр'),
)

class Goods(models.Model):
    title = models.CharField(max_length=100)
    ed = models.CharField(max_length=5,choices=ED_CHOICES)
    section = models.ForeignKey(Section, null=True, blank=True)
    descr = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return "%s" % (self.title)

    class Meta:
        ordering = ["title"]


CURR_CHOICES = (
    ('rur','руб'),
    ('usd','usd'),
    ('eur','eur'),
)

class Trade(models.Model):
    user = models.ForeignKey(User)
    shop = models.ForeignKey(Shop)
    goods = models.ForeignKey(Goods)
    time = models.DateTimeField(default=datetime.now) #(auto_now_add=True)
    time_add = models.DateTimeField(default=datetime.now,editable=False)
    amount = models.FloatField()
    price = models.DecimalField(max_digits=19, decimal_places=2)
    currency = models.CharField(max_length=3,choices=CURR_CHOICES)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    spytrade = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s" % ( self.goods.__unicode__() + " " + unicode(self.amount) )

    class Meta:
        ordering = ["-time"]


class TradeForm(forms.Form):
    trade_pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    spytrade = forms.BooleanField(label="Подсмотрено", required=False)
    time = forms.DateTimeField(label="Время", required=True)
    shop = forms.CharField(max_length=100, required=True, label="Торговая точка")
    shop_pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    gtitle = forms.CharField(max_length=50, required=True, label="Наименование")
    gtitle_pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    ed = forms.ChoiceField(choices=ED_CHOICES, label="Единица измерения")
    amount = forms.FloatField(required=True, label="Количество")
    cost = forms.DecimalField(max_digits=12, decimal_places=2, required=True, label="Стоимость")
    currency = forms.ChoiceField(choices=CURR_CHOICES, label="Валюта")
    
