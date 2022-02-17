from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import ProductViewSet, Question_2ViewSet, Question_3ViewSet, AllMyProductsViewSet, PricesViewSet, UserViewSet, ProductAllDataViewSet, ProductAllDataCompetitorViewSet, CompetitorViewSet, bypassORM, MyView, ProductAllDataCompetitorViewSet1, Question_1ViewSet


router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('products', ProductViewSet)  # it's the DataMainTable with all the data inside
router.register('products_allData', ProductAllDataViewSet, basename='DataMainTable_allData')  # it's the DataMainTable with all the data inside
router.register('products_allDataCompetitors', ProductAllDataCompetitorViewSet, basename='CompetitorAnalysisModel_retry')
router.register('Question_1', Question_1ViewSet, basename='test')
router.register('Question_2', Question_2ViewSet, basename='test')
router.register('Question_3', Question_3ViewSet, basename='test')
router.register('allMyProducts', AllMyProductsViewSet) # it's the products list
router.register('allMyCompetitors', CompetitorViewSet)
router.register('prices', PricesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
