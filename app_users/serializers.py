from rest_framework import serializers
from .models import User
import base64
import uuid
from django.core.files.base import ContentFile


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{uuid.uuid4()}.{ext}')
        return super().to_internal_value(data)

class UserSerializer(serializers.ModelSerializer):
    photo_url = Base64ImageField(max_length=None, use_url=True,) 

    class Meta:
        model = User
        fields = ['id','email','password','username','finger_print', 'noms', 'photo_url', 'profile']
        #fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        print("USER", validated_data)
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.is_active = False
        instance.profile_id = 1
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.profile_id = 1
        instance.save()
        return instance
