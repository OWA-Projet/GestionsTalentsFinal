from ..models import Contact

class ServiceContact:
    @staticmethod
    def create_contact(validated_data):
        return Contact.objects.create(**validated_data)
