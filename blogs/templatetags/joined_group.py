from atexit import register
from tokenize import group
from django import template
from blogs.models import GroupJoined, Group, User

register= template.Library()
@register.filter(name='joined_group')
def joined_group(groupid, username):
    group_obj= Group.objects.get(id=groupid)
    user_obj= User.objects.get(username=username)
    joinedgroup= GroupJoined.objects.filter(joined_group=group_obj, joined_by= user_obj)
    if joinedgroup.exists():
        return True
    return False