from rest_framework import serializers
from .models import DataMainTable, AllMyProducts, Prices, DataMainTable_allData, CompetitorList, test, CompetitorAnalysisModel_retry
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):   # for creating new users
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)  # automatically creates a token for every user that is created
        return user

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataMainTable
        fields = ('id', 'product', 'my_price', 'my_productName', 'price', 'date')

class ProductAllDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataMainTable_allData
        fields = ('id', 'product', 'company', 'my_price', 'my_productName', 'price', 'date')

class ProductAllDataCompetitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataMainTable_allData
        fields = ('id', 'my_productName', 'company', 'my_price')

class CompetitorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitorList
        fields = ('CompetitorID', 'CompetitorName')

class AllMyProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllMyProducts
        fields = ('id', 'NameOfProduct', 'NameOfMyProduct', 'productMyUrl', 'productSkroutzUrl', 'no_of_prices', 'avg_prices')

class PricesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prices
        fields = ('id', 'product', 'user', 'price')


class Question1serializer(serializers.ModelSerializer):
    class Meta:
        model = test
        fields = ('CityId', 'id', 'weather_state_name', 'weather_state_abbr', 'wind_direction_compass', 'created', 'applicable_date', 'min_temp', 'max_temp', 'the_temp', 'wind_speed', 'wind_direction', 'air_pressure', 'humidity', 'visibility', 'predictability')

class Question2serializer(serializers.ModelSerializer):
    class Meta:
        model = test
        fields = ('id', 'CityId', 'applicable_date', 'the_temp')

class Question3serializer(serializers.ModelSerializer):
    class Meta:
        model = test
        fields = ('id', 'CityId', 'applicable_date', 'the_temp', 'weather_state_name')




# after making the serializers you need to go to the views to make views for each of my serializers