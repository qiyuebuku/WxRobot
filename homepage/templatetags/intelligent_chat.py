from django import template
register=template.Library()
@register.simple_tag
def gender_caught (sex):
    print(sex)
    if sex == "男":
        return "male"
    elif sex == "女":
        return "female"
    else:
        return "secrecy"