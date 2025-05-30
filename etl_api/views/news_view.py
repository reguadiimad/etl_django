# api/views/news_views.py

from rest_framework import generics
from ..models.news import News
from ..serializers.news_serializers import NewsSerializer
from ..serializers.NewsTranslatedSerializer import NewsTranslatedSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class NewsCreateView(generics.CreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsTranslatedListView(APIView):
    def get(self, request):
        news_items = News.objects.all()
        serializer = NewsTranslatedSerializer(news_items, many=True)
        return Response(serializer.data)


class NewsUpdateView(generics.UpdateAPIView):
    """
    PUT /api/news/<pk>/update/    -> full update
    PATCH /api/news/<pk>/update/  -> partial update
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsDeleteView(generics.DestroyAPIView):
    """
    DELETE /api/news/<pk>/delete/
    Delete a News item.
    """
    queryset = News.objects.all()
    serializer_class = NewsSerializer