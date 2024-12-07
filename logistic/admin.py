from django.contrib import admin
from django.db import models

from logistic.models import Product, Stock


class StockInline(admin.TabularInline):
    model = Stock.products.through
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description_column', 'quantity_column']
    list_display_links = ['title']
    inlines = [StockInline]

    @admin.display(description='Описание', ordering='description')
    def description_column(self, obj):
        len_ = 20
        return obj.description[:len_] + ('...' if len(obj.description) > len_ else '')
    
    @admin.display(description='Количество складов', ordering='stocks_number')
    def quantity_column(self, obj):
        return obj.stocks_number

    def get_queryset(self, request):
        return Product.objects.annotate(stocks_number=models.Count('stocks'))


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['id', 'address']
    list_display_links = ['address']
    inlines = [StockInline]