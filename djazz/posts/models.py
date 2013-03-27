from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site


class PostManager(models.Manager):
    pass

class Post(models.Model):
    
    title = models.CharField(max_length=240, null=True, blank=True)
    sites = models.ManyToManyField(Site)
    lang = models.CharField(max_length=10, null=True, blank=True)
    encoding = models.CharField(max_length=20, null=True, blank=True)
    parent = models.ForeignKey('self', related_name='post_parent',
                               null=True, blank=True)
    author = models.ForeignKey(User, related_name="post_author",
                               null=True, blank=True)
    date = models.DateTimeField()
    tz = models.CharField(max_length=20)
    last_editor = models.ForeignKey(User,null=True, blank=True,
                                    related_name="post_last_editor")
    last_date = models.DateTimeField()
    last_tz = models.CharField(max_length=20)
    content = models.TextField(null=True, blank=True)
    type = models.CharField(max_length=25, blank=True, null=True)
    format = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=15, null=True, blank=True)
    
    objects = PostManager()
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        t = getattr(self, 'TYPE', None)
        if not self.type:
            self.type = t
        super(Post, self).save(*args, **kwargs)
    
    def to_html(self):
        from django.template import Context, loader
        from django.conf import settings
        from djazz.posts import defaults
        
        if not self.format:
            f = 'default'
        else:
            f = self.format
        
        # Defaults formatters
        mapped = defaults.DJAZZ_FORMATTERS
        fdef = defaults.DJAZZ_FORMATTERS['default']
        
        # Getting tpl formatter
        mapped.update(getattr(settings, 'DJAZZ_FORMATTERS', {}))
        try:
            tplfile = mapped[f]
        except:
            tplfile = fdef
        
        # Format content
        c = Context({'text': self.content})
        try:
            template = loader.get_template(tplfile)
        except:
            # Formatter not exist, try to format with default formatter
            try:
                template = loader.get_template(fdef)
            except:
                raise
        
        return template.render(c)


class PostVarManager(models.Manager):
    pass

class PostVar(models.Model):
    post    = models.ForeignKey('Post',related_name="postvar_post")
    key     = models.CharField(max_length=60)
    value   = models.TextField(null=True,blank=True)
    objects = PostVarManager()
    
    def __unicode__(self):
        return self.key + " - " + self.post.title

    
