from django.contrib import admin

from cooking.models import Receipts, Ingredients


class ReceiptAdmin(admin.ModelAdmin):
    list_display = ("rec_title", "author", "rating", "process")
    list_filter = ("rec_title", )


admin.site.register(Receipts, ReceiptAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("quantity", "unit", "ingr_name", "price")
    list_filter = ("ingr_name", )

admin.site.register(Ingredients, IngredientAdmin)