from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models.condidats import Condidats
from ..serializers.condidats_serializers import CondidatsSerializer

@api_view(['GET', 'POST'])
def condidats_view(request):
    if request.method == 'GET':
        condidats = Condidats.objects.all()
        serializer = CondidatsSerializer(condidats, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CondidatsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
