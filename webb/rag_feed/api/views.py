# webb/rag_feed/api/views.py

from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from django.db.models import Q

from djangoplicity.pages.models import Page
from .serializers import PageRagFeedSerializer
from djangoplicity.releases.models import Release
from .serializers import ReleaseRagFeedSerializer
from djangoplicity.announcements.models import Announcement
from .serializers import AnnouncementRagFeedSerializer

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

class ReleaseListAPIView(ListAPIView):
    """
    View to expose the content of public Press Releases.
    """
    serializer_class = ReleaseRagFeedSerializer
    pagination_class = RagFeedPagination

    def get_queryset(self):
        """
        Filters to return only published releases that have
        passed their release date (embargo).
        """
        now = timezone.now()
        return Release.objects.filter(
            Q(published=True) &
            (Q(release_date__isnull=True) | Q(release_date__lte=now))
        ).order_by('-release_date')

class AnnouncementListAPIView(ListAPIView):
    """
    View to expose the content of public Announcements.
    """
    serializer_class = AnnouncementRagFeedSerializer
    pagination_class = RagFeedPagination

    def get_queryset(self):
        """
        Filters the queryset to return only published announcements
        that have passed their release date (embargo).
        """
        now = timezone.now()
        return Announcement.objects.filter(
            Q(published=True) &
            (Q(release_date__isnull=True) | Q(release_date__lte=now))
        ).order_by('-release_date')
