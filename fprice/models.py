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

class City(models.Model):
    title = models.CharField(max_length=50)
    country = models.ForeignKey(Country)

    def __unicode__(self):
        return self.title

class Street(models.Model):
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title

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
    
    def __unicode__(self):
        return "%s" % ( self.addr.city.title + " - " + self.title + " (" + self.addr.__unicode__() +")")

class GSection(models.Model):
    title = models.CharField(max_length=50)

    def __unicode__(self):
        return self.title
        
class GClass(models.Model):
    title = models.CharField(max_length=50)
    section = models.ForeignKey(GSection)

    def __unicode__(self):
        return self.title

class Goods(models.Model):
    GOODS_CHOICES = (
        ('prd','продукты'),
        ('ode','одежда'),
        ('med','медицина'),
    )
    ED_CHOICES = (
        ('sh', 'шт/уп'),
        ('kg', 'кг'),
        ('gr', 'грамм'),        
        ('m', 'метр'),
        ('l', 'литр'),
    )
    gclass = models.ForeignKey(GClass, null=True, blank=True)
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=3,choices=GOODS_CHOICES, null=True, blank=True)
    descr = models.TextField(null=True, blank=True)
    ed = models.CharField(max_length=5,choices=ED_CHOICES)
    
    def __unicode__(self):
        return "%s" % ( self.gclass.title + " - " + self.title )

class Trade(models.Model):
    CURR_CHOICES = (
        ('rur','рубли'),
        ('usd','доллары'),
        ('eur','евро'),
    )
    user = models.ForeignKey(User)
    shop = models.ForeignKey(Shop)
    goods = models.ForeignKey(Goods)
    time = models.DateTimeField(default=datetime.now) #(auto_now_add=True)
    amount = models.FloatField()
    price = models.DecimalField(max_digits=19, decimal_places=2)
    currency = models.CharField(max_length=3,choices=CURR_CHOICES)
    
    def __unicode__(self):
        return "%s" % ( self.goods.__unicode__() + " " + unicode(self.amount) )

class TradeForm(forms.Form):
    gclass = forms.CharField(max_length=50)
