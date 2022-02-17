from django.contrib import admin
from .models import AllMyProducts, DataMainTable, Prices, DataMainTable_allData, CompetitorList, CompetitorAnalysisModel_retry


# add the models here in order to be visible from the admin page

# @admin.register(DataMainTable)
# class ProductAdmin(admin.ModelAdmin):
#     list_display =  ['product', 'my_price', 'price']

admin.site.register(AllMyProducts)
admin.site.register(DataMainTable)
admin.site.register(DataMainTable_allData)
admin.site.register(Prices)
admin.site.register(CompetitorList)
admin.site.register(CompetitorAnalysisModel_retry)