from django import template
import project

register = template.Library()


@register.filter
def viewable(filename):
    return project.models.viewable(filename)
