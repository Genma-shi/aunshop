from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CartItem
from .serializers import CartItemSerializer
from books.models import Book
from stationery.models import Stationery
from promotions.models import Promotion

class CartListView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    def get_queryset(self):
        user = self.request.user if self.request.user.is_authenticated else None
        session_key = self.request.session.session_key if not user else None
        return CartItem.objects.filter(user=user) | CartItem.objects.filter(session_key=session_key)

class CartAddView(APIView):
    serializer_class = CartItemSerializer
    def post(self, request):
        item_type = request.data.get('item_type')
        item_id = request.data.get('item_id')
        quantity = int(request.data.get('quantity', 1))
        user = request.user if request.user.is_authenticated else None
        session_key = request.session.session_key if not user else None
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        kwargs = {'user': user, 'session_key': session_key}
        if item_type == 'book':
            kwargs['book'] = Book.objects.get(id=item_id)
        elif item_type == 'stationery':
            kwargs['stationery'] = Stationery.objects.get(id=item_id)
        elif item_type == 'promotion':
            kwargs['promotion'] = Promotion.objects.get(id=item_id)
        else:
            return Response({"detail": "Invalid item type"}, status=status.HTTP_400_BAD_REQUEST)
        cart_item, created = CartItem.objects.get_or_create(**kwargs, defaults={'quantity': quantity})
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return Response(CartItemSerializer(cart_item).data)

class CartRemoveView(APIView):
    serializer_class = CartItemSerializer
    def delete(self, request, pk):
        user = request.user if request.user.is_authenticated else None
        session_key = request.session.session_key if not user else None
        cart_item = CartItem.objects.filter(id=pk).filter(user=user) | CartItem.objects.filter(id=pk).filter(session_key=session_key)
        if cart_item.exists():
            cart_item.delete()
            return Response({"detail": "Item removed"})
        return Response({"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND)