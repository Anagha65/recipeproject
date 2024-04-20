from .models import *
from rest_framework import serializers

class RecipiesSerializers(serializers.ModelSerializer):
    Recip_img=serializers.ImageField(required=False)
    class Meta:
        model=Recipes
        fields='__all__'


