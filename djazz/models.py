from django.db import models

class ConfigManager(models.Manager):
    
    def getvar(self, key, section=''):
        if section == None:
            return self.filter(key=key)
        else:
            return self.get_or_create(key=key,section=section)[0]
    
    def setvar(self, key, value, section=''):
        c = self.get_or_create(key=key, section=section)[0]
        c.value = value
        c.save()
    
    def delvar(self, key, section=''):
        q = self.filter(key=key)
        if section:
            q = q.filter(section=section)
        q.delete()


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
