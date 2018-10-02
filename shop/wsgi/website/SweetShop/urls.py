from django.conf.urls import url
from . import views

app_name = 'SweetShop'

# the different url patterns that redirect users to the view function associated with the entered url.
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^products/$', views.products, name='products'),
    url(r'^basket/$', views.basket, name='basket'),
    url(r'^(?P<product_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^addtobasket/$', views.addtobasket, name='addtobasket'),
    url(r'^delete_item/$', views.delete_item, name='delete_item'),
    url(r'^quantity_update/$', views.quantity_update, name='quantity_update'),
    url(r'^checkout/$', views.checkout, name='checkout'),
]
