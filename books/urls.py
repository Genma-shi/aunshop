from django.urls import path
from .views import BookListView, BookDetailView , SubjectListView , BookListWithFiltersView , FiltersDataView

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('subjects/', SubjectListView.as_view(), name='subject_list'),
    path('books-with-filters/', BookListWithFiltersView.as_view(), name='books_with_filters'),
    path('filters-data/', FiltersDataView.as_view(), name='filters_data'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
]