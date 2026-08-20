# webb/rag_feed/api/serializers.py

from rest_framework import serializers
from bs4 import BeautifulSoup
from djangoplicity.pages.models import Page
from djangoplicity.releases.models import Release
from djangoplicity.announcements.models import Announcement
from djangoplicity.newsletters.models import Newsletter

class RagFeedBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer to standardize the RAG feed output.
    """
    url = serializers.SerializerMethodField()
    text_content = serializers.SerializerMethodField()

    class Meta:
        fields = ('title', 'url', 'date_created', 'last_modified', 'text_content')
        abstract = True

    def get_url(self, obj):
        """
        Gets the absolute URL of the object.
        """
        if hasattr(obj, 'get_absolute_url'):
            request = self.context.get('request')
            return request.build_absolute_uri(obj.get_absolute_url())
        return None

    def get_text_content(self, obj):
        """
        Extracts and cleans HTML content to return only plain text.
        """
        # It will look for a 'content' field by default.
        # This can be overridden in child serializers if the content field has a different name.
        html_content = getattr(obj, 'content', '')
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        return ''

class PageRagFeedSerializer(RagFeedBaseSerializer):
    """
    Serializer for the Page model.
    """
    date_created = serializers.DateTimeField(source='created')

    class Meta(RagFeedBaseSerializer.Meta):
        model = Page
        fields = RagFeedBaseSerializer.Meta.fields

class ReleaseRagFeedSerializer(RagFeedBaseSerializer):
    """
    Serializer for the Release model (Press Releases).
    """
    date_created = serializers.DateTimeField(source='release_date')

    class Meta(RagFeedBaseSerializer.Meta):
        model = Release
        fields = RagFeedBaseSerializer.Meta.fields

    def get_text_content(self, obj):
        """
        Extracts and cleans HTML content from the 'description' field.
        """
        html_content = getattr(obj, 'description', '')
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        return ''

class AnnouncementRagFeedSerializer(RagFeedBaseSerializer):
    """
    Serializer for the Announcement model.
    """
    date_created = serializers.DateTimeField(source='release_date')

    class Meta(RagFeedBaseSerializer.Meta):
        model = Announcement
        fields = RagFeedBaseSerializer.Meta.fields

    def get_text_content(self, obj):
        """
        Extracts and cleans HTML content from the 'description' field.
        """
        html_content = getattr(obj, 'description', '')
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        return ''


class NewsletterRagFeedSerializer(RagFeedBaseSerializer):
    """
    Serializer for the Newsletter model.
    """
    # Newsletters use 'subject' instead of 'title'
    title = serializers.CharField(source='subject')
    date_created = serializers.DateTimeField(source='release_date')

    class Meta(RagFeedBaseSerializer.Meta):
        model = Newsletter
        fields = RagFeedBaseSerializer.Meta.fields

    def get_text_content(self, obj):
        """
        Extracts and cleans HTML content.
        Prioritizes the 'html' field, falls back to 'text' if empty.
        """
        content = getattr(obj, 'html', '')
        if not content:
            content = getattr(obj, 'text', '')

        if content:
            soup = BeautifulSoup(content, 'html.parser')
            return soup.get_text(separator=' ', strip=True)
        return ''
