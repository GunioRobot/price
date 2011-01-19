#!/usr/bin/env python
# -*- coding: utf-8 -*-

from address.models import Country, City, Street, Address
from django.contrib import admin

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Street)
admin.site.register(Address)
