from django.db import models
from django.core.cache import cache

class ConfigManager(models.Manager):
    
    def getvar(self, key, section=''):
        if section == None:
            return self.filter(key=key)
        else:
            cachedkey = '.'.join([section, key])
            if cache.has_key(cachedkey):
                return cache.get(cachedkey)
            else:
                return self.get_or_create(key=key,section=section)[0]
    
    def setvar(self, key, value, section=''):
        cachedkey = '.'.join([section, key])
        c = self.get_or_create(key=key, section=section)[0]
        c.value = value
        c.save()
        cache.set(cachedkey, value)
    
    def delvar(self, key, section=''):
        cachedkey = '.'.join([section, key])
        q = self.filter(key=key)
        if section:
            q = q.filter(section=section)
        q.delete()
        cache.delete(cachedkey)


class Config(models.Model):
    section = models.CharField(max_length=60, blank=True)
    key = models.CharField(max_length=60)
    value = models.TextField(null=True, blank=True)
    objects = ConfigManager()
    
    class Meta:
        unique_together = (('section', 'key'))
    
    def __unicode__(self):
        section = self.section or ''
        return '['+section+'] '+self.key

