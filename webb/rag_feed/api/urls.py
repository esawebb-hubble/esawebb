# webb/rag_feed/api/urls.py

from django.conf.urls import url
from .views import (
    PageListAPIView,
    ReleaseListAPIView,
    AnnouncementListAPIView,
    NewsletterListAPIView  # Add this
)

urlpatterns = [
    # Endpoint for Pages
    url(r'^pages/$', PageListAPIView.as_view(), name='rag-feed-pages'),
    url(r'^releases/$', ReleaseListAPIView.as_view(), name='rag-feed-releases'),
    url(r'^announcements/$', AnnouncementListAPIView.as_view(), name='rag-feed-announcements'),
    url(r'^newsletters/$', NewsletterListAPIView.as_view(), name='rag-feed-newsletters'),
]
