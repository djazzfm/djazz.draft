
class MenuItem(object):
    def __init__(self, id, label, url,
                 weight=0,
                 parent=None,
                 **kwargs):
        self.id = str(id)
        self.label = label
        self.url = url
        self.weight = weight
        self.parent = str(parent)
        self.args = kwargs


class Menu(object):
    
    def __init__(self, title=None, items=[], **kwargs):
        self.title = title
        self.args = kwargs
        
        self._items = []
        self._index = {}
        self._childs = {}
        
        for item in items:
            self.additem(item)
    
    def additem(self, item):
        if not isinstance(item, MenuItem):
            raise Exception('MenuItem instance expected')
        
        if item.id in self._index:
            message = 'Item %s is already registered' % str(item.id)
            raise Exception(message)
        
        self._items.append(item)
        self._index[item.id] = item
        if not item.id in self._childs:
            self._childs[item.id] = []
        if item.parent:
            if not item.parent in self._childs:
                self._childs[item.parent] = []
            self._childs[item.parent].append(item)
    
    def items(self, items=None, level=0,
              key=lambda item: item.weight,
              reverse=False,
              cmp=None):
        
        filtereds = []
        
        if not items:
            items = []
            for item in self._items:
                if not item.parent or not item.parent in self._index:
                    items.append(item)
        
        items = sorted(items,key=key,reverse=reverse,cmp=None)
        count = len(items)
        for i in range(count):
            item = items[i]
            
            filtereds.append({'item': item,
                              'level': level,
                              'first': i == 0,
                              'last': i == count - 1})
            
            if len(self._childs[item.id]) > 0:
                childs = self.items(self._childs[item.id],
                                    level=level+1,
                                    key=key,
                                    reverse=reverse,
                                    cmp=cmp)
                filtereds = filtereds + childs
        return filtereds
    
    
    def render(self, template='djazz/menu.html', context = {}):
        from django.template import Context, loader
        
        context['menu'] = self
        context['items'] = self.items()
        t = loader.get_template(template)
        
        return t.render(Context(context))
