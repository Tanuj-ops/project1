from django.contrib import admin
from project.models import category, register_table, add_product ,cart, order,feature_product
admin.site.site_header = "ArtGallery"
class categoryAdmin(admin.ModelAdmin):
    list_display = ("id", "cat_name", "description", "added_on")
    search_fields = ('cat_name',)
admin.site.register(category, categoryAdmin)
admin.site.register(register_table) 
admin.site.register(add_product)  
admin.site.register(cart) 
admin.site.register(order) 
admin.site.register(feature_product) 
