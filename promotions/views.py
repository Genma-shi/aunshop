from rest_framework import generics
from .models import Promotion
from .serializers import PromotionSerializer

class PromotionListView(generics.ListAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

class PromotionDetailView(generics.RetrieveAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer