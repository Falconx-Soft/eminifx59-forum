from atexit import register
from django import template
from blogs.models import PostComment,Post, CommentReply
register= template.Library()
@register.filter(name='replies')
def replies(id):
    comment= PostComment.objects.filter(id=id)
    if comment.exists():
        all_replies=CommentReply.objects.filter(comment=comment[0])
        return all_replies
    return None