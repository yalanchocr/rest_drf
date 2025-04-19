from django.contrib import admin
from myapp.models import Product, Task, ChildProduct

# @admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # list_display = ("q_task_id", "")
    list_display = [field.name for field in Task._meta.fields]

    # list_display = [field.name for field in Task._meta.fields]
# Register your models here.

# admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # list_display = ("q_task_id", "")
    list_display = [field.name for field in Product._meta.fields]
    date_hierarchy = "created_at"
    fields = [("name", "price"), "in_stock"]    


admin.site.register(ChildProduct)

admin.site.register(Task, TaskAdmin)
