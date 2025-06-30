from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.ContactSerializer import ContactSerializer
from ..services.ServiceContact import ServiceContact

class ContactAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            contact = ServiceContact.create_contact(serializer.validated_data)
            return Response(ContactSerializer(contact).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
