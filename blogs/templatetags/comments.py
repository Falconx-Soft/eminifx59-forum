from atexit import register
from django import template
from blogs.models import PostComment,Post
register= template.Library()
@register.filter(name='comments')
def comments(id):
    post= Post.objects.filter(id=id)
    if post.exists():
        all_comments=PostComment.objects.filter(blog=post[0])
        return all_comments
    return None