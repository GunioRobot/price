#from django.conf.urls.defaults import *

#urlpatterns = patterns('',
    #(r'^info/$', 'defapp.views.index'),
    #(r'^$', 'defapp.views.logo'),
#)

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from fprice.views import trade_last_list, trade_add, trade_view, shop_info, trade_goods_list

urlpatterns = patterns('fprice.views',
    # Example:
    # (r'^openprice/', include('openprice.foo.urls')),

    (r'^$', 'trade_last_list'),
    (r'^trade/add/', 'trade_add'),
    (r'^trade/(?P<trade_id>\d+)', 'trade_view'),
    (r'^shop/(?P<shop_id>\d+)', 'shop_info'),
    (r'^goods/(?P<goods_id>\d+)', 'trade_goods_list'),
    (r'^accounts/', include('registration.urls')),    

    url(r'^title_lookup/', 'shop_title_lookup', name='title_lookup'),

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
