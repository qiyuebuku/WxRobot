from django import template
from django.utils.safestring import mark_safe 

register = template.Library()

@register.simple_tag
def filter_shop(plug,user_plugs):
    tag = """
    <button style="float:right" type="button" class="btn btn-lg {0}" {3} value="{1}">{2}</button>
    """
    print('---------filter_shop------------')
    print(plug,user_plugs,end="\n")
    for user_plug in user_plugs:
        print(user_plug)
        if plug == user_plug.plug:
            tag = tag.format("btn-default disabled",plug.id,"已拥有","")
            break
    else:
        tag = tag.format("btn-success",plug.id,"获&nbsp;&nbsp;&nbsp;取","onclick=get_more_plugins(this);")
    return mark_safe(tag)
    