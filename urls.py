#from django.conf.urls.defaults import *

#urlpatterns = patterns('',
    #(r'^info/$', 'defapp.views.index'),
    #(r'^$', 'defapp.views.logo'),
#)

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from fprice.views import trade_last_list, trade_add, shop_info, trade_goods_list

urlpatterns = patterns('fprice.views',
    # Example:
    # (r'^openprice/', include('openprice.foo.urls')),

    (r'^$', 'trade_last_list'),
    (r'^trade/add/', 'trade_add'),
    (r'^shop/(?P<shop_id>\d+)', 'shop_info'),
    (r'^goods/(?P<goods_id>\d+)', 'trade_goods_list'),
    (r'^accounts/', include('registration.urls')),    

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)