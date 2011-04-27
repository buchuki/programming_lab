from django import template
import project

register = template.Library()


@register.filter
def viewable(filename):
    return project.models.viewable(filename)

@register.filter
def editable(filename):
    return project.models.editable(filename)

@register.filter
def extension(filename):
    return project.models.extension(filename)

@register.filter
def admin_link(user):
    if user.is_anonymous():
        return False
    if user.is_superuser:
        return True
    if user.instructed_classes.count():
        return True
    if user.classtutor_set.count():
        return True
    return False
