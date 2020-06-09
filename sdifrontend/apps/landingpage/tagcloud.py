from django import template

register = template.Library()

class TagCloud:
    def __init__(self):
        self.keywords = ["tag","cloud"]


@register.simple_tag(takes_context=True)
def get_tag_cloud_keywords(context, **kwargs):
    tc = TagCloud()
    return tc.keywords
