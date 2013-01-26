from django import template

register = template.Library()


@register.filter(name='range')
def filter_range(value, arg="0, 1"):
    arg = str(arg)
    start = 0
    stop = int(value)
    step = 1
    
    args = arg.split(',')
    args.reverse()
    
    if len(args) > 0:
        start = int(args.pop().strip())
    
    if len(args) > 0:
        step = int(args.pop().strip())
    
    return range(start, stop, step)


@register.filter(name='indexof')
def filter_index(index, tab):
    try:
        return tab[index]
    except:
        return None

@register.filter(name='attrof')
def filter_attr(attr, obj):
    return getattr(obj, attr, None)
