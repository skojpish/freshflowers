from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="administration"),
    path("excel", views.excel_input, name="excel_input"),
    path("excelconfirm", views.excel_confirm, name="excel_confirm"),
    path("pricelist", views.price_list, name="price_list"),
    path("pricelistconfirm", views.price_list_confirm, name="price_list_confirm"),
]