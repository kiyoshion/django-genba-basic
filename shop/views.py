from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import View

from .models import Book

class IndexView(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    queryset = Book.objects.select_related('publisher').prefetch_related('authors').order_by('publish_date')
    keyword = request.GET.get('keyword')
    if keyword:
      queryset = queryset.filter(
        Q(title__icontains=keyword)
      )
    context = {
      'keyword': keyword,
      'book_list': queryset,
    }
    return render(request, 'shop/book_list.html', context)

index = IndexView.as_view()

class DetailView(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    book = Book.objects.get(pk=book_id)
    context = {
      'book': book,
    }
    return render(request, 'shop/book_detail.html', context)

detail = DetailView.as_view()

class CheckoutView(LoginRequiredMixin, View):
  def post(self, request, *args, **kwargs):
    import time
    start_time = time.time()

    item_id = request.POST['item_id']
    book = get_object_or_404(Book, pk=item_id)

    return render(request, 'shop/complete.html')

checkout = CheckoutView.as_view()
