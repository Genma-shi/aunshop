# core/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from books.models import Book
from books.serializers import BookSerializer
from stationery.models import Stationery
from stationery.serializers import StationeryListSerializer
from .models import PageContent
from .serializers import PageContentSerializer

class GlobalSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"detail": "Parameter not specified ?q="}, status=status.HTTP_400_BAD_REQUEST)

        books = Book.objects.filter(Q(title__icontains=query))
        stationeries = Stationery.objects.filter(Q(title__icontains=query))

        return Response({
            "books": BookSerializer(books, many=True).data,
            "stationery": StationeryListSerializer(stationeries, many=True).data,
        })

class PageContentDetailView(APIView):
    def get(self, request, key):
        try:
            page = PageContent.objects.get(key=key)
        except PageContent.DoesNotExist:
            return Response({"detail": "Page not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PageContentSerializer(page)
        return Response(serializer.data)