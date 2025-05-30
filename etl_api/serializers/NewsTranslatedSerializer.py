# api/serializers/news_translated_serializer.py
from rest_framework import serializers
from deep_translator import GoogleTranslator
from django.core.cache import cache # Import Django's cache
import logging # For logging errors

from ..models.news import News

logger = logging.getLogger(__name__)

def translate_text(text, target_language, source_language='fr'):
    if not text: # Don't try to translate empty strings
        return text

    # Use a hash of the text for a more manageable cache key, if texts are very long
    # For moderately sized text, the text itself can be part of the key.  
    # Be mindful of cache key length limits if text is very long.
    cache_key = f"translation_{source_language}_to_{target_language}_{hash(text)}"
    translated_text = cache.get(cache_key)

    if translated_text is not None:
        return translated_text
    try:
        translated_text = GoogleTranslator(source=source_language, target=target_language).translate(text)
        cache.set(cache_key, translated_text, timeout=60*60*24) # Cache for 24 hours
        return translated_text
    except Exception as e:
        logger.error(f"Translation failed for text '{text[:50]}...' to {target_language}: {e}", exc_info=True)
        return text # Fallback if translation fails

class NewsTranslatedSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    article = serializers.SerializerMethodField()
    publish_by = serializers.CharField(source='published_by')
    # publish_date field is missing from your original fields list but present in Meta
    # Make sure it's intended or remove it.
    # Assuming you might want it formatted:
    publish_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True) # Or DateField if it's just a date
    news_date = serializers.DateField(format="%Y-%m-%d")
    schoolYear = serializers.CharField(source='school_year')
    isPinned = serializers.BooleanField(source='is_pinned')
    imgSrc = serializers.CharField(source='img_url')

    class Meta:
        model = News
        fields = [
            'id', # Good to include the ID
            'publish_by',
            'publish_date', # Added based on typical needs
            'tag',
            'title',
            'description',
            'article',
            'news_date',
            'schoolYear',
            'isPinned',
            'imgSrc'
        ]

    def get_translated_field(self, obj, field_name):
        original_text = getattr(obj, field_name, None) # Use getattr with default
        if original_text is None: # Handle if field doesn't exist or is None
             return {'fr': None, 'en': None, 'ar': None}

        # Retrieve target languages from context if dynamic, or define statically
        # For example, if languages could be passed in the request:
        # target_languages = self.context.get('target_languages', ['en', 'ar'])
        # For now, using fixed 'en' and 'ar' as in your original code.

        translations = {'fr': original_text}
        translations['en'] = translate_text(original_text, 'en')
        translations['ar'] = translate_text(original_text, 'ar')
        return translations

    def get_tag(self, obj):
        return self.get_translated_field(obj, 'tag')

    def get_title(self, obj):
        return self.get_translated_field(obj, 'title')

    def get_description(self, obj):
        return self.get_translated_field(obj, 'description')

    def get_article(self, obj):
        return self.get_translated_field(obj, 'article')