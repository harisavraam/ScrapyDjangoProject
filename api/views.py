import os
import sys
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import action
from .models import DataMainTable, AllMyProducts, Prices, DataMainTable_allData, CompetitorList, CompetitorAnalysisModel_retry, test
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ProductSerializer, AllMyProductsSerializer, Question3serializer, Question2serializer, UserSerializer,CompetitorListSerializer, PricesSerializer, ProductAllDataSerializer, ProductAllDataCompetitorSerializer, Question1serializer
from rest_framework.authentication import TokenAuthentication
from scrapyd_api import ScrapydAPI
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods
from scrapy.utils.project import get_project_settings
from pathlib import Path
import django_rq
from scrapy.crawler import CrawlerProcess, Crawler, CrawlerRunner
from scrapy_app.scrapy_app import settings as my_settings
from scrapy_app.scrapy_app.spiders.icrawler import IcrawlerSpider
from scrapy_app.scrapy_app.spiders import icrawler
from scrapy.utils.log import configure_logging
from crochet import setup
from scrapy.settings import Settings
from twisted.internet import reactor
from scrapy import signals
import os
from django.http import JsonResponse
from django.db import connection
from rest_framework import mixins, viewsets
from collections import namedtuple
from django.shortcuts import render
from django.db import connections



# connect scrapyd service
scrapyd = ScrapydAPI('http://localhost:6800/')

@csrf_exempt
@require_http_methods(['POST', 'GET'])
def crawl(request):
    # for scrapyd that doesn't work
    # settings = {
    #     'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
    # }
    task = scrapyd.schedule('default', 'icrawler')
    # return JsonResponse({'task_id': task, 'status': 'started'})
    # crawler_settings = get_project_settings()
    # process = CrawlerRunner(crawler_settings)
    # process.crawl(icrawler.IcrawlerSpider)



# after making the views we need to register our viewsets to urls.py to a new router
# request.user is here

def my_custom_sql(self):
    with connection.cursor() as cursor:
        cursor.callproc('CompetitorAnalysis1', [self.production_name])
        row = cursor.fetchall()
    return row

# 13-12-2021
cursor = connection.cursor()
def stored_proc(req):
    cursor.execute('')


class bypassORM(viewsets.ModelViewSet):
    model = CompetitorAnalysisModel_retry
    def list(self, request):
        product_name = self.request.query_params.get('product_name')
        print(product_name)
        cursor = connection.cursor()
        queryset = CompetitorAnalysisModel_retry.objects.raw('call CompetitorAnalysis1', [product_name])
        # cursor.callproc('CompetitorAnalysis1', [product_name])
        # queryset = cursor.fetchall()
        serializer = ProductAllDataCompetitorSerializer(queryset, many=True)
        print(queryset)
        return Response(serializer.data)


class MyView(viewsets.ViewSet):


    def get(self, request):
        def execute_to_dict(query, params=None):
            with connection.cursor() as c:
                c.execute(query, params or [])
                names = [col[0] for col in c.description]
                return [dict(list(zip(names, values))) for values in c.fetchall()]
        product_name = self.request.query_params.get('product_name')
        print(product_name)
        data = execute_to_dict(
             "SELECT a, b FROM x WHERE y = %s AND z = %s"
             ["yvalue", 73]
        )
        return Response({
            'count': len(data),
            'results': data
        })

class ProductAllDataCompetitorViewSet1(viewsets.ViewSet):
    # viewsets.ViewSet, APIView, mixins.ListModelMixin, viewsets.GenericViewSet
    # serializer_class = ProductAllDataCompetitorSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )
    print('activated')




    def get_queryset(self):
        def dictfetchall(cursor):
            desc = cursor.description
            return [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]

        def namedtuplefetchall(cursor):
            "Return all rows from a cursor as a namedtuple"
            desc = cursor.description
            nt_result = namedtuple('Result', [col[0] for col in desc])
            return [nt_result(*row) for row in cursor.fetchall()]
            product_name = self.request.query_params.get('product_name')
            print(product_name)
        # name_map = {'distinctCompany': 'distinctCompany','countCompany': 'countCompany','countCompanyPerCent': 'countCompanyPerCent'}
        # queryset = CompetitorAnalysisModel_retry.objects.raw('call CompetitorAnalysis(%s)', [product_name], translations=name_map)
        # queryset = CompetitorAnalysisModel_retry.objects.raw('call CompetitorAnalysis(%s)', [product_name])

        # queryset = CompetitorAnalysisModel_retry.objects.raw('SELECT DISTINCT(company) as distinctCompany, COUNT(id) as countCompany, COUNT(id) / (SELECT COUNT(id) FROM skroutz_4.api_datamaintable_alldata WHERE replace(product, \'+\', \'\') = %s) as countCompanyPerCent FROM skroutz_4.api_datamaintable_alldata WHERE replace(product, \'+\', \'\') = %s group by distinctCompany;', [product_name, product_name])
        cursor = connection.cursor()
        # cursor.execute('call CompetitorAnalysis(%s)', [product_name])
        # cursor.callproc('CompetitorAnalysis1', [product_name])
        # 13122021 edited cursor.execute('SELECT DISTINCT(company) as distinctCompany, COUNT(id) as countCompany, COUNT(id) / (SELECT COUNT(id) FROM skroutz_4.api_datamaintable_alldata WHERE replace(product, \'+\', \' \') = %s) as countCompanyPerCent FROM skroutz_4.api_datamaintable_alldata WHERE replace(product, \'+\', \' \') = %s group by distinctCompany;',[product_name, product_name])
        queryset = dictfetchall(cursor)
        # queryset = namedtuplefetchall(cursor)
        # queryset = cursor.fetchall()
        print(queryset)
        # serializer = ProductAllDataCompetitorSerializer(queryset)
        return queryset



class ProductAllDataCompetitorViewSet(viewsets.ModelViewSet):
    # viewsets.ViewSet, viewsets.ModelViewSet, APIView, mixins.ListModelMixin-viewsets.GenericViewSet
    serializer_class = ProductAllDataCompetitorSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )




    def get_queryset(self):
        product_name = self.request.query_params.get('product_name')
        print(product_name)
        def dictfetchall(cursor):
            desc = cursor.description
            return [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]

        def namedtuplefetchall(cursor):
            "Return all rows from a cursor as a namedtuple"
            desc = cursor.description
            nt_result = namedtuple('Result', [col[0] for col in desc])
            return [nt_result(*row) for row in cursor.fetchall()]

        # name_map = {'distinctCompany': 'distinctCompany','countCompany': 'countCompany','countCompanyPerCent': 'countCompanyPerCent'}
        # queryset = CompetitorAnalysisModel_retry.objects.raw('call CompetitorAnalysis(%s)', [product_name], translations=name_map)
        # queryset = CompetitorAnalysisModel_retry.objects.raw('call CompetitorAnalysis(%s)', [product_name])
        # queryset = CompetitorAnalysisModel_retry.objects.raw('SELECT DISTINCT(company) as distinctCompany, COUNT(id) as countCompany, COUNT(id) / (SELECT COUNT(id) FROM skroutz_4.api_datamaintable_alldata WHERE replace(product, \'+\', \'\') = %s) as countCompanyPerCent FROM skroutz_4.api_datamaintable_alldata WHERE replace(product, \'+\', \'\') = %s group by distinctCompany;', [product_name, product_name])
        # cursor.execute('call CompetitorAnalysis(%s)', [product_name])
        cursor = connection.cursor()
        cursor.callproc('CompetitorAnalysisSOS5', [product_name])
        queryset = dictfetchall(cursor)
        # cursor.execute('SELECT DISTINCT(company) as id, COUNT(id) as product, COUNT(id) / (SELECT COUNT(id) FROM skroutz_4.api_datamaintable_alldata WHERE replace(product, \'+\', \' \') = %s) as company FROM skroutz_4.api_datamaintable_alldata WHERE replace(product, \'+\', \' \') = %s group by id;',[product_name, product_name])
        # queryset = namedtuplefetchall(cursor)
        # queryset = cursor.fetchall()
        print(queryset)
        # serializer = ProductAllDataCompetitorSerializer(queryset)
        return queryset


class Question_1ViewSet(viewsets.ModelViewSet):
    serializer_class = Question1serializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )




    def get_queryset(self):
        product_name = self.request.query_params.get('name')
        print(product_name)
        def dictfetchall(cursor):
            desc = cursor.description
            return [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]

        def namedtuplefetchall(cursor):
            "Return all rows from a cursor as a namedtuple"
            desc = cursor.description
            nt_result = namedtuple('Result', [col[0] for col in desc])
            return [nt_result(*row) for row in cursor.fetchall()]


        cursor = connection.cursor()
        cursor.close()
        cursor = connection.cursor()
        cursor.callproc('Question_1')
        queryset = dictfetchall(cursor)
        print(queryset)
        return queryset

class Question_2ViewSet(viewsets.ModelViewSet):
    serializer_class = Question2serializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )




    def get_queryset(self):
        product_name = self.request.query_params.get('name')
        print(product_name)
        def dictfetchall(cursor):
            desc = cursor.description
            return [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]

        def namedtuplefetchall(cursor):
            "Return all rows from a cursor as a namedtuple"
            desc = cursor.description
            nt_result = namedtuple('Result', [col[0] for col in desc])
            return [nt_result(*row) for row in cursor.fetchall()]


        cursor = connection.cursor()
        cursor.close()
        cursor = connection.cursor()
        cursor.callproc('Question_2')
        queryset = dictfetchall(cursor)
        print(queryset)
        return queryset

class Question_3ViewSet(viewsets.ModelViewSet):
    serializer_class = Question3serializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )




    def get_queryset(self):
        NumberOfLocations = self.request.query_params.get('NumberOfLocations')
        print(NumberOfLocations)
        def dictfetchall(cursor):
            desc = cursor.description
            return [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]

        def namedtuplefetchall(cursor):
            "Return all rows from a cursor as a namedtuple"
            desc = cursor.description
            nt_result = namedtuple('Result', [col[0] for col in desc])
            return [nt_result(*row) for row in cursor.fetchall()]


        cursor = connection.cursor()
        cursor.callproc('Question_3', NumberOfLocations)
        queryset = dictfetchall(cursor)
        print(queryset)
        return queryset




class CompetitorAnalysisView(APIView):
    def competitorAnalysis(self, request, product_name=None):
        product_name = self.request.query_params.get('product_name')
        print(product_name)
        cursor = connection.cursor()
        cursor.callproc('CompetitorAnalysis1', [product_name])
        queryset = cursor.fetchall()
        print(queryset)
        return queryset

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)   # AllowAny or isAuthenticated


class CompetitorViewSet(viewsets.ModelViewSet):
    queryset = CompetitorList.objects.all()
    serializer_class = CompetitorListSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = DataMainTable.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )

class ProductAllDataViewSet(viewsets.ModelViewSet):
    serializer_class = ProductAllDataSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )

    def get_queryset(self):
        def dictfetchall(cursor):
            desc = cursor.description
            return [
                dict(zip([col[0] for col in desc], row))
                for row in cursor.fetchall()
            ]
        queryset = DataMainTable_allData.objects.all()
        product_name = self.request.query_params.get('product_name')
        print(product_name)
        if product_name is not None:
            # queryset = DataMainTable_allData.objects.raw('SELECT * FROM skroutz_4.api_datamaintable_alldata WHERE replace(product, \'+\', \' \') LIKE CONCAT (\'%\', %s, \'%\')', [product_name])
            # queryset = DataMainTable_allData.objects.raw('call ProductTimeSeries(%s)', product_name)
            cursor = connection.cursor()
            cursor.callproc('ProductTimeSeries', [product_name])
            queryset = dictfetchall(cursor)
        return queryset
        # if product_name is not None:
        #     queryset = DataMainTable_allData.objects.filter(product=product_name)
        #     return queryset
        # else:
        #     queryset = DataMainTable_allData.objects.all()
        #     return queryset

        # queryset = DataMainTable_allData.objects.all()
        # product_name = self.request.query_params.get('product_name')
        # if product_name is not None:
        #     queryset = queryset.filter(product=product_name)
        # return queryset




class AllMyProductsViewSet(viewsets.ModelViewSet):
    queryset = AllMyProducts.objects.all()
    serializer_class = AllMyProductsSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )

    @action(detail=True, methods=['POST'])
    def price_product(self, request, pk=None):
        if 'price' in request.data:
            product = AllMyProducts.objects.get(id=pk)
            price = request.data['price']
            user = request.user
            print('user ', user)
            # user = User.objects.get(id=2)
            print('user', user.username)    # or NameOfMyProduct

            try:
                prices = Prices.objects.get(user=user.id, product=product.id)
                prices.price = price
                prices.save()
                serializer = PricesSerializer(prices, many=False)
                response = {'message': 'Price updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                prices = Prices.objects.create(user=user, product=product, price=price)
                serializer = PricesSerializer(prices, many=False)
                response = {'message': 'Price created', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = {'message': 'You need to provide price'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)



class PricesViewSet(viewsets.ModelViewSet):
    queryset = Prices.objects.all()
    serializer_class = PricesSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def update(self, request, *args, **kwargs):
        response = {'message': 'You cant update price like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {'message': 'You cant create price like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


