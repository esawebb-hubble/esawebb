# webb/rag_feed/api/serializers.py

from rest_framework import serializers
from bs4 import BeautifulSoup
from djangoplicity.pages.models import Page

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
