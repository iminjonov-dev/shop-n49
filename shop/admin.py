from django.contrib.auth.models import User, Group
from django.contrib import admin

from shop.models import Category, Product, Comment

# admin.site.register(Product)
# admin.site.register(Category)
admin.site.register(Comment)


# admin.site.unregister(User)
admin.site.unregister(Group)

class IsVeryExpensiveFilter(admin.SimpleListFilter):
    title = 'Is Very Expensive Product'
    parameter_name = 'is_very_expensive_product'


    def lookups(self, request, model_admin):
        return (('Yes', 'Yes'), ('No', 'No'))

def queryset(self, request, queryset):
    value = self.value()
    if value == 'Yes':
        return queryset.filter(pric__gte=20_000_000)
    elif value == 'No':
        return queryset.filter(pric__gte=20_000_000)
    return queryset

@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    search_fields = ('title', 'id')
    # exclude = ('slug',)
    prepopulated_fields = {"slug": ("title",)}


    def product_count(self, obj):
        return obj.product.count()


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'discount', 'is_very_expensive_product')
    search_fields = ['name']
    # list_filter = ['category', IsVeryExpensiveFilter]
    def is_very_expensive_product(self, obj):
        return obj.price > 20_000_000

    is_very_expensive_product.boolean = True