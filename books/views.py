from rest_framework import generics, filters , viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book , Subject 
from .serializers import BookSerializer , SubjectSerializer
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['book_class', 'language', 'subject']
    search_fields = ['title', 'author']

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['language', 'book_class', 'subject']  # Фильтрация по языку, классу, предмету
    search_fields = ['title']  # Поиск по названию

class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

LANGUAGE_CHOICES = [
    ('KG', 'Кыргызский'),
    ('RU', 'Русский'),
    ('EN', 'Английский'),
]

CLASS_CHOICES = [
    ('preschool', 'Дошкольный'),
    ('1', '1 класс'),
    ('2', '2 класс'),
    ('3', '3 класс'),
    ('4', '4 класс'),
    ('5', '5 класс'),
    ('6', '6 класс'),
    ('7', '7 класс'),
    ('8', '8 класс'),
    ('9', '9 класс'),
    ('10', '10 класс'),
    ('11', '11 класс'),
]

class BookListWithFiltersView(APIView):
    def get(self, request):
        qs = Book.objects.all()

        book_class = request.GET.get('book_class')
        language = request.GET.get('language')
        subject = request.GET.get('subject')
        search = request.GET.get('search')

        if book_class:
            qs = qs.filter(book_class=book_class)
        if language:
            qs = qs.filter(language=language)
        if subject:
            qs = qs.filter(subject_id=subject)
        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(author__icontains=search))

        books_serializer = BookSerializer(qs, many=True, context={'request': request})
        subjects = Subject.objects.all()
        subjects_serializer = SubjectSerializer(subjects, many=True)

        data = {
            'books': books_serializer.data,
            'filters': {
                'languages': [{'key': k, 'label': v} for k, v in LANGUAGE_CHOICES],
                'classes': [{'key': k, 'label': v} for k, v in CLASS_CHOICES],
                'subjects': subjects_serializer.data,
            }
        }
        return Response(data)

class FiltersDataView(APIView):
    def get(self, request):
        subjects = Subject.objects.all()
        subjects_serializer = SubjectSerializer(subjects, many=True)

        data = {
            'languages': [{'key': k, 'label': v} for k, v in LANGUAGE_CHOICES],
            'classes': [{'key': k, 'label': v} for k, v in CLASS_CHOICES],
            'subjects': subjects_serializer.data,
        }
        return Response(data)