from pprint import pp

from django.db.models import F, Q, QuerySet
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import (CustomSerializer, ProductSerializer,
                                  StockSerializer)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # при необходимости добавьте параметры фильтрации
    filterset_fields = ['title']
    search_fields = ['title', 'description']

class StockViewSet(ModelViewSet):
    queryset: QuerySet = Stock.objects.prefetch_related('products', 'positions')
    serializer_class = StockSerializer
    # при необходимости добавьте параметры фильтрации
    filterset_fields = ['products']
    search_fields = ['products__title', 'products__description']
    
    def list(self, request, *args, **kwargs):
        queryset: QuerySet = self.filter_queryset(self.get_queryset())

        if param := request.GET.get('products'):
            queryset = queryset.annotate(
                    quantity=F('positions__quantity'),
                    price=F('positions__price'),
                    product=F('products__title'))
            self.serializer_class = CustomSerializer

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
