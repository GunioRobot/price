#!/usr/bin/env python
# -*- coding: utf-8 -*-

from models import Country, City, Street, Address, Center, Shop, GSection, GClass, Goods, Trade
from django.contrib import admin

class TradeAdmin(admin.ModelAdmin):

    actions = ['make_spy']

    def make_spy(self, request, queryset):
        rows_updated = queryset.update(spytrade=True)
        if rows_updated == 1:
            message_bit = "1 покупка была"
        else:
            message_bit = "%s покупок было" % rows_updated
        self.message_user(request, "%s отмечено как подсмотренные." % message_bit)

    make_spy.short_description = "Пометить как подсмотренные"


admin.site.register(Country)
admin.site.register(City)
admin.site.register(Street)
admin.site.register(Address)
admin.site.register(Center)
admin.site.register(Shop)
admin.site.register(GSection)
admin.site.register(GClass)
admin.site.register(Goods)
admin.site.register(Trade, TradeAdmin)
