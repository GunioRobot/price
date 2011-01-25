#!/usr/bin/env python
# -*- coding: utf-8 -*-

from price.models import Section, Goods, Price, Trade
from django.contrib import admin

class TradeAdmin(admin.ModelAdmin):

    actions = ['make_spy']

    def make_spy(self, request, queryset):
        rows_updated = queryset.update(spytrade=True)
        #if rows_updated == 1:
        #    message_bit = "1 покупка была"
        #else:
        #    message_bit = "%s покупок было" % rows_updated
        #self.message_user(request, "%s отмечено как подсмотренные." % message_bit)

    make_spy.short_description = "Mark as spy"

admin.site.register(Section)
admin.site.register(Goods)
admin.site.register(Price)
admin.site.register(Trade, TradeAdmin)
