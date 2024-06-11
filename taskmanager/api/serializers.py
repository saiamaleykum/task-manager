from rest_framework import serializers

from .models import Task, User


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'phone', 'groups', 'role']
        extra_kwargs = {
            'password': {'write_only': True},  
        }


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']  


class CustomerTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description']  

    def create(self, validated_data):
        validated_data['customer'] = self.context['request'].user  
        return super().create(validated_data)

    
class EmployeeTaskCreateSerializer(serializers.ModelSerializer):
    customer_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(groups__name='customer'), source='customer')

    class Meta:
        model = Task
        fields = ['title', 'description', 'customer_id']
