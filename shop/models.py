#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from address.models import Address


"""class Network(models.Model):
    title = models.CharField(max_length=100)
    descr = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["title"]"""


class Center(models.Model):
    title = models.CharField(max_length=100)
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
        ('zap', 'заправка'),
    )
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=3,choices=SHOP_CHOICES)
    center = models.ForeignKey(Center, null=True, blank=True)
    #network = models.ForeignKey(Network, null=True, blank=True)
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