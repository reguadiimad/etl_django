from rest_framework import generics
from ..models.admin import Inscription
from ..serializers.inscription_serializers import InscriptionSerializer

class InscriptionListView(generics.ListAPIView):
    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer

class InscriptionDetailView(generics.RetrieveAPIView):
    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer


class InscriptionCreateView(generics.CreateAPIView):
    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer
