from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.contact_serializers import ContactFormSerializer
from ..models.contact import ContactForm

class ContactFormView(APIView):
    def post(self, request):
        serializer = ContactFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Form submitted successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactFormListView(APIView):
    def get(self, request):
        contact_forms = ContactForm.objects.all()
        serializer = ContactFormSerializer(contact_forms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
