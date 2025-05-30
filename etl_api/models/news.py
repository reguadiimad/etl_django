from django.db import models

class News(models.Model):
    # auto-incrementing primary key `id` is created automatically
    published_by = models.CharField(max_length=100)
    publish_date = models.DateTimeField(auto_now_add=True)
    news_date = models.DateField()
    tag = models.CharField(max_length=2000)
    title = models.CharField(max_length=2000)
    description = models.TextField(max_length=2000)
    article = models.TextField()
    school_year = models.CharField(max_length=9)  # e.g. "2024-2025"
    is_pinned = models.BooleanField(default=False)
    img_url = models.URLField(max_length=2000, blank=True)

    class Meta:
        ordering = ['-publish_date']
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return f"{self.title} ({self.news_date})"
