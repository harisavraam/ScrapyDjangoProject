from django.db import models
from django.contrib.auth.models import User

# after making the models you need to register them in admin.py of the api app

# class Products(models.Model):
#      NameOfProduct = models.CharField(max_length=255, default='NULL', blank=False)
#      NameOfMyProduct = models.CharField(max_length=255, blank=False)
#      productMyUrl = models.CharField(max_length=255, blank=False)
#      productSkroutzUrl = models.CharField(max_length=255, blank=False)
#      myNewPrice = models.DecimalField(default=0, max_digits=18, decimal_places=8)
#      # class Meta:
#      #     unique_together = (('NameOfProduct', 'productMyUrl', 'productSkroutzUrl'))
#      #     index_together = (('NameOfProduct', 'productMyUrl', 'productSkroutzUrl'))
#
class AllMyProducts(models.Model):
     NameOfProduct = models.CharField(max_length=255, blank=False)
     NameOfMyProduct = models.CharField(max_length=255, blank=True)
     productMyUrl = models.CharField(max_length=255, blank=True)
     productSkroutzUrl = models.CharField(max_length=255, blank=True)

     def no_of_prices(self):
         prices = Prices.objects.filter(product=self)
         return len(prices)

     def avg_prices(self):
         sum=0
         prices = Prices.objects.filter(product=self)
         for i in prices:
             sum += i.price
         if len(prices) > 0:
            return sum / len(prices)
         else:
             return 0



class CompetitorAnalysisModel_retry(models.Model):
    distinctCompany: models.CharField(max_length=100, primary_key=True)
    countCompany: models.IntegerField()
    countCompanyPerCent: models.DecimalField(max_digits=18, decimal_places=8)


class CompetitorList(models.Model):
    CompetitorID = models.CharField(max_length=100, primary_key=True)
    CompetitorName = models.CharField(max_length=100)

class DataMainTable(models.Model):
    product = models.CharField(max_length=255, blank=False)
    my_price = models.DecimalField(default=0, max_digits=18, decimal_places=8)
    my_productName = models.CharField(max_length=255, blank=False)
    my_availability = models.CharField(max_length=255)
    company = models.IntegerField()
    price = models.DecimalField(default=0, max_digits=18, decimal_places=8)
    bestPriceAvailability = models.CharField(max_length=255)
    date = models.DateTimeField()

class DataMainTable_allData(models.Model):
    product = models.CharField(max_length=255, blank=False)
    my_price = models.DecimalField(default=0, max_digits=18, decimal_places=8)
    my_productName = models.CharField(max_length=255, blank=False)
    my_availability = models.CharField(max_length=255)
    company = models.IntegerField()
    price = models.DecimalField(default=0, max_digits=18, decimal_places=8)
    bestPriceAvailability = models.CharField(max_length=255)
    date = models.DateTimeField()

class Prices(models.Model):
    product = models.ForeignKey(AllMyProducts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(blank=True, max_digits=18, decimal_places=8)

    class Meta:
        unique_together = (('user', 'product'),)
        index_together = (('user', 'product'),)



class test(models.Model):
    CityId = models.CharField(max_length=50, blank=False)
    id = models.CharField(max_length=100, blank=False, primary_key=True)
    weather_state_name = models.CharField(max_length=100, blank=False)
    weather_state_abbr = models.CharField(max_length=100, blank=False)
    wind_direction_compass = models.CharField(max_length=100, blank=False)
    created = models.DateTimeField()
    applicable_date = models.DateField()
    min_temp = models.DecimalField(max_digits=24, decimal_places=14)
    max_temp = models.DecimalField(max_digits=24, decimal_places=14)
    the_temp = models.DecimalField(max_digits=24, decimal_places=14)
    wind_speed = models.DecimalField(max_digits=24, decimal_places=14)
    wind_direction = models.DecimalField(max_digits=24, decimal_places=14)
    air_pressure = models.DecimalField(max_digits=24, decimal_places=14)
    humidity = models.IntegerField()
    visibility = models.DecimalField(max_digits=24, decimal_places=14)
    predictability = models.IntegerField()
