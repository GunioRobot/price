#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    (r'^$', 'price.views.trade_list' ),
    (r'^trade/add/', 'price.views.trade_add'),
    (r'^trade/(?P<trade_id>\d+)', 'price.views.trade_view'),
    (r'^goods/(?P<goods_id>\d+)', 'price.views.trade_by_goods' ),
    (r'^shop/(?P<shop_id>\d+)', 'shop.views.trade_by_shop'),
    (r'^accounts/', include('registration.urls')),
    url(r'^profile/', 'price.views.trade_by_user', name='user_profile'),
    (r'^search/$', 'price.views.search'),
    url(r'^lookup/(shop|goods)', 'price.views.lookup', name='json_lookup'),
    url(r'^edit/goods/', 'price.views.edit_goods', name='edit_goods'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

# routing static files
from django.conf import settings
if settings.LOCALSERVER:
    urlpatterns+= patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True})
    )
