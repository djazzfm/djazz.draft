from django import template
register = template.Library()

class MetasNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    
    def render(self, context):
        import json
        if not 'metas' in context:
            context['metas'] = {}
        output = '{ '+self.nodelist.render(context)+' }'
        context['metas'].update(json.loads(output))
        return ''

def set_metas(parser, token):
    nodelist = parser.parse(('endpostmetas',))
    parser.delete_first_token()
    return MetasNode(nodelist)

register.tag('postmetas', set_metas)
