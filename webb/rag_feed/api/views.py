# webb/rag_feed/api/views.py

from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from django.db.models import Q

from djangoplicity.pages.models import Page
from .serializers import PageRagFeedSerializer

class RagFeedPagination(PageNumberPagination):
    """
    Custom pagination for the RAG feed endpoints.
    """
    page_size = 500
    page_size_query_param = 'page_size'
    max_page_size = 1000

class PageListAPIView(ListAPIView):
    """
    View to expose the content of public Pages.
    """
    serializer_class = PageRagFeedSerializer
    pagination_class = RagFeedPagination

    def get_queryset(self):
        """
        Filters the queryset to return only pages that are published
        and within their publication window (no embargo).
        """
        now = timezone.now()
        return Page.objects.filter(
            Q(published=True) &
            (Q(start_publishing__isnull=True) | Q(start_publishing__lte=now)) &
            (Q(end_publishing__isnull=True) | Q(end_publishing__gte=now))
        ).order_by('-last_modified')
