from rest_framework import serializers

class ContactUsSerailizer(serializers.Serializer):
    full_name = serializers.CharField()
    email = serializers.EmailField()
    subject = serializers.CharField()
    message = serializers.CharField()