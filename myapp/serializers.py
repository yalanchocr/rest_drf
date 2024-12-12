from .models import Product, Task
from django.conf import settings
from rest_framework import serializers



class ProductSerializer(serializers.ModelSerializer):
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields  = '__all__'
        extra_kwargs = {'photo': {'write_only': True}}  # Hide photo field in response

    def get_photo_url(self, obj):
        request = self.context.get('request')
        if obj.photo:
            return request.build_absolute_uri(obj.photo.url)
        return None


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        # fields = '__all__'
        fields = ['q_task_id', 'title', 'status', 'meta_data', 'created_at']

        # fields = ['q_task_id',]  # Customize fields for creation/update
        # Add extra validation or logic if needed



#
# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'



# class ProductCreateUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['name', 'price', 'in_stock', 'photo']  # Customize fields for creation/update
#         # Add extra validation or logic if needed




