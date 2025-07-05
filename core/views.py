# core/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
<<<<<<< HEAD

=======
>>>>>>> d27e09a2c0be8f10faa03f7cadeb3f330d7b5baa
from books.models import Book
from books.serializers import BookSerializer
from stationery.models import Stationery
from stationery.serializers import StationeryListSerializer
<<<<<<< HEAD
from promotions.models import Promotion
from promotions.serializers import PromotionSerializer
=======

>>>>>>> d27e09a2c0be8f10faa03f7cadeb3f330d7b5baa

class GlobalSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"detail": "Не указан параметр ?q="}, status=status.HTTP_400_BAD_REQUEST)

        books = Book.objects.filter(Q(title__icontains=query))
        stationeries = Stationery.objects.filter(Q(title__icontains=query))
<<<<<<< HEAD
        promotions = Promotion.objects.filter(Q(title__icontains=query))
=======
>>>>>>> d27e09a2c0be8f10faa03f7cadeb3f330d7b5baa

        return Response({
            "books": BookSerializer(books, many=True).data,
            "stationery": StationeryListSerializer(stationeries, many=True).data,
<<<<<<< HEAD
            "promotions": PromotionSerializer(promotions, many=True).data,
=======
>>>>>>> d27e09a2c0be8f10faa03f7cadeb3f330d7b5baa
        })
 