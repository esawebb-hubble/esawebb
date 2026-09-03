    # webb/rag_feed/api/urls.py

from django.conf.urls import url
from .views import (
    PageListAPIView,
    ReleaseListAPIView,
    AnnouncementListAPIView,
    NewsletterListAPIView,
    ScienceAnnouncementListAPIView,
    ImageListAPIView,
    POTWListAPIView,
    ImageComparisonListAPIView,
    VideoListAPIView,
    BookListAPIView,
    BrochureListAPIView
)

urlpatterns = [
    # Endpoint for Pages
    url(r'^pages/$', PageListAPIView.as_view(), name='rag-feed-pages'),
    url(r'^releases/$', ReleaseListAPIView.as_view(), name='rag-feed-releases'),
    url(r'^announcements/$', AnnouncementListAPIView.as_view(), name='rag-feed-announcements'),
    url(r'^newsletters/$', NewsletterListAPIView.as_view(), name='rag-feed-newsletters'),
    url(r'^science-announcements/$', ScienceAnnouncementListAPIView.as_view(), name='rag-feed-science-announcements'),
    url(r'^media/images/$', ImageListAPIView.as_view(), name='rag-feed-media-images'),
    url(r'^media/potm/$', POTWListAPIView.as_view(), name='rag-feed-media-potws'),
    url(r'^media/comparisons/$', ImageComparisonListAPIView.as_view(), name='rag-feed-media-comparisons'),
    url(r'^media/videos/$', VideoListAPIView.as_view(), name='rag-feed-media-videos'),
    # Products
    url(r'^products/books/$', BookListAPIView.as_view(), name='rag-feed-books'),
    url(r'^products/brochures/$', BrochureListAPIView.as_view(), name='rag-feed-brochures'),
]
