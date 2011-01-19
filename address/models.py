#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


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

    # TODO: full office returning

    def __unicode__(self):
        return "%s" % ( self.street.title + " " + unicode(self.house) )