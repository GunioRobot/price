#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django import forms

class Country(models.Model):
    title = models.CharField(max_length=50)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["title"]


class City(models.Model):
    title = models.CharField(max_length=50)
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["title"]


class Street(models.Model):
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["title"]


class Address(models.Model):
    city = models.ForeignKey(City)
    street = models.ForeignKey(Street)
    house = models.CharField(max_length=10)
    housing = models.CharField(max_length=10, null=True, blank=True)
    office = models.CharField(max_length=10, null=True, blank=True)
    x = models.FloatField(null=True, blank=True)
    y = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return "%s" % ( self.street.title + " " + unicode(self.house) )


class Center(models.Model):
    title = models.CharField(max_length=50)
    descr = models.TextField(null=True, blank=True)
    addr = models.ForeignKey(Address)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["title"]


class Shop(models.Model):
    SHOP_CHOICES = (
        ('mag', 'магазин'),
        ('ksk', 'киоск'),
        ('otd', 'отдел'),
    )
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=3,choices=SHOP_CHOICES)
    center = models.ForeignKey(Center, null=True, blank=True)
    addr = models.ForeignKey(Address, null=True, blank=True)

    def get_addr(self):
        res = ''
        if self.addr:
            res = self.addr.city.title + ', ' + self.addr.street.title + ', ' + self.addr.house
        return res

    def __unicode__(self):
        return "%s (%s)" % (self.title, self.get_addr())

    class Meta:
        ordering = ["title"]


class GSection(models.Model):
    title = models.CharField(max_length=50)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["title"]


class GClass(models.Model):
    title = models.CharField(max_length=50)
    section = models.ForeignKey(GSection)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["title"]


ED_CHOICES = (
    ('sh', 'шт'),
    ('kg', 'кг'),
    ('gr', 'грамм'),
    ('m', 'метр'),
    ('l', 'литр'),
)

class Goods(models.Model):
    GOODS_CHOICES = (
        ('prd','продукты'),
        ('ode','одежда'),
        ('med','медицина'),
    )
    gclass = models.ForeignKey(GClass, null=True, blank=True)
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=3,choices=GOODS_CHOICES, null=True, blank=True)
    descr = models.TextField(null=True, blank=True)
    ed = models.CharField(max_length=5,choices=ED_CHOICES)

    def __unicode__(self):
        #if self.gclass:
        #    return "%s" % ( self.gclass.title + " - " + self.title )
        #else:
        return "%s" % (self.title)

    class Meta:
        ordering = ["title"]


CURR_CHOICES = (
    ('rur','рубли'),
    ('usd','доллары'),
    ('eur','евро'),
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


class TradeForm(forms.Form):
    trade_pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    spytrade = forms.BooleanField(label="Подсмотрено")
    time = forms.DateTimeField(label="Время", required=True)
    shop = forms.CharField(max_length=100, required=True, label="Торговая точка")
    shop_pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    #gclass = forms.CharField(max_length=50, required=True, label="Тип продукта/услуги")
    #gclass_pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    gtitle = forms.CharField(max_length=50, required=True, label="Наименование")
    gtitle_pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    ed = forms.ChoiceField(choices=ED_CHOICES, label="Единица измерения")
    amount = forms.FloatField(required=True, label="Количество")
    cost = forms.DecimalField(max_digits=12, decimal_places=2, required=True, label="Стоимость")
    currency = forms.ChoiceField(choices=CURR_CHOICES, label="Валюта")
    #price = forms.DecimalField(max_digits=12,decimal_places=2,required=False, label="Цена")
