from django.db import models
from django.core.cache import cache
from django.db.models.signals import pre_delete
from django.dispatch import receiver


def get_cached_key(key, section=None):
    if section == None:
        section = ''
    return '.'.join(['djazzconfig', str(section), str(key)])

def get_cached_id(uid):
    return '.'.join(['djazzconfigid', str(uid)])


class ConfigManager(models.Manager):
    
    def getvar(self, key, section=None):
        cachedkey = get_cached_key(key, section)
        if cache.has_key(cachedkey):
            return cache.get(cachedkey)
        else:
            var = self.get_or_create(key=key, section=section)[0]
            return var.value
    
    def setvar(self, key, value, section=None):
        c = self.get_or_create(key=key, section=section)[0]
        c.value = value
        c.save()
    
    def delvar(self, key, section=None):
        self.filter(key=key, section=section).delete()


class Config(models.Model):
    section = models.CharField(max_length=60, blank=True)
    key = models.CharField(max_length=60)
    value = models.TextField(null=True, blank=True)
    objects = ConfigManager()
    
    class Meta:
        unique_together = (('section', 'key'))
    
    def __unicode__(self):
        section = self.section or ''
        return section+'.'+self.key
    
    def clear_config_cache(self):
        if self.id and cache.has_key(get_cached_id(self.id)):
            cached_id = get_cached_id(self.id)
            cached_key = cache.get(cached_id)
            cache.delete(cached_id)
            cache.delete(cached_key)
    
    def create_config_cache(self):
        if not self.id: return;
        cached_key = get_cached_key(self.key, self.section)
        cached_id = get_cached_id(self.id)
        cache.set(cached_id, cached_key)
        cache.set(cached_key, str(self.value))
    
    def save(self, *args, **kwargs):
        self.clear_config_cache()
        super(Config, self).save(*args, **kwargs)
        self.create_config_cache()

@receiver(pre_delete)
def configvar_delete(sender, **kwargs):
    obj = kwargs['instance']
    if isinstance(obj, Config):
        obj.clear_config_cache()
