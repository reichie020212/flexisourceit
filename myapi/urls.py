from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^registration/$', views.RegistrationView.as_view()),
    url(r'^login/$', views.LoginView.as_view()),
    url(r'^stock/$', views.StockListView.as_view()),
    url(r'^stock/create/$', views.StockCreateView.as_view()),
    url(r'^stock/(?P<pk>\d+)/$', views.StockUpdateView.as_view()),
    url(r'^stock/buy/$', views.BuyStockView.as_view()),
    url(r'^stock/sell/$', views.SellStockView.as_view()),
    url(r'^stock/list/$', views.MyStockListView.as_view()),
    url(r'^stock/total/$', views.MyStockTotalInvestedView.as_view()),
]