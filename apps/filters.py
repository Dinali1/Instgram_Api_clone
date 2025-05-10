import django_filters
from .models import Post

class PostFilter(django_filters.FilterSet):
    post_type = django_filters.CharFilter(field_name='post_type', lookup_expr='exact')

    class Meta:
        model = Post
        fields = ['post_type']