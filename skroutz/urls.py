from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', obtain_auth_token),
    # path('api/crawl/', views.crawl, name='crawl'),
    path('competitors', views.CompetitorAnalysisView, name='competitorAnalysis'),

]
