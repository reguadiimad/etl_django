from rest_framework import generics
from ..models.inscription import Inscription
from ..serializers.inscription_serializers import InscriptionSerializer
from ..serializers.InscriptionConfirmSerializer import InscriptionConfirmSerializer

class InscriptionListView(generics.ListAPIView):
    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer

class InscriptionDetailView(generics.RetrieveUpdateAPIView):  # ✅ changed here
    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer

class InscriptionCreateView(generics.CreateAPIView):
    queryset = Inscription.objects.all()
    serializer_class = InscriptionSerializer
# views.py
class InscriptionUpdateView(generics.UpdateAPIView):
    queryset = Inscription.objects.all()
    serializer_class = InscriptionConfirmSerializer
    lookup_field = 'id'  # Or 'pk' if you're using that in URL
    http_method_names = ['patch', 'put']
