from django.db import connection
from rest_framework.views import APIView
from django.views.decorators.http import require_POST, require_http_methods
from collections import namedtuple




class CompetitorAnalysisView(APIView):
    def competitorAnalysis(self, request, product_name=None):
        product_name = self.request.query_params.get('product_name')
        print(product_name)
        cursor = connection.cursor()
        cursor.callproc('CompetitorAnalysis1', [product_name])
        queryset = cursor.fetchall()
        print(queryset)
        return queryset

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
        cursor.execute(
            'SELECT DISTINCT(company) as distinctCompany, COUNT(id) as countCompany, COUNT(id) / (SELECT COUNT(id) FROM skroutz_4.api_datamaintable_alldata WHERE replace(product, \'+\', \' \') = %s) as countCompanyPerCent FROM skroutz_4.api_datamaintable_alldata WHERE replace(product, \'+\', \' \') = %s group by distinctCompany;',
            [product_name, product_name])

        queryset = namedtuplefetchall(cursor)
        # queryset = cursor.fetchall()
        print(queryset)
        # serializer = ProductAllDataCompetitorSerializer(queryset)
        return queryset