# core/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from books.models import Book
from books.serializers import BookSerializer
from stationery.models import Stationery
from stationery.serializers import StationeryListSerializer
from .models import PageContent , ContactPhoneNumber
from .serializers import PageContentSerializer , ContactPhoneNumberSerializer
from utils.notifications import send_fcm_notification
from rest_framework.decorators import api_view

class GlobalSearchView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"detail": "Parameter not specified ?q="}, status=status.HTTP_400_BAD_REQUEST)

        books = Book.objects.filter(Q(title__icontains=query))
        stationeries = Stationery.objects.filter(Q(title__icontains=query))

        books_data = BookSerializer(books, many=True, context={'request': request}).data
        stationeries_data = StationeryListSerializer(stationeries, many=True, context={'request': request}).data

        return Response({
            "books": books_data,
            "stationery": stationeries_data,
        })

class PageContentDetailView(APIView):
    def get(self, request, key):
        try:
            page = PageContent.objects.get(key=key)
        except PageContent.DoesNotExist:
            return Response({"detail": "Page not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PageContentSerializer(page)
        return Response(serializer.data)
    
class ContactPhoneNumberView(APIView):
    def get(self, request):
        phone = ContactPhoneNumber.objects.first()
        if not phone:
            return Response({"phone_number": None})
        return Response(ContactPhoneNumberSerializer(phone).data)

@api_view(['POST'])
def test_push(request):
    fcm_token = request.data.get('fcm_token')  # можно получить откуда-то
    send_fcm_notification(
        title="🔔 Тест!",
        body="Это тестовое уведомление",
        fcm_token=fcm_token,
        sound="default",
        data={"test": "123"}
    )
    return Response({"ok": True})