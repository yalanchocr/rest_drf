from django.contrib import admin
from myapp.models import Product, Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("q_task_id",)
    # list_display = [field.name for field in Task._meta.fields]
# Register your models here.

admin.site.register(Product)
# admin.site.register(Task, TaskAdmin)
