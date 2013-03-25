from django.db import models
from django.contrib.auth.models import User


class PostManager(models.Manager):
    pass

class Post(models.Model):
    
    title = models.CharField(max_length=240, null=True, blank=True)
    lang = models.CharField(max_length=10, null=True, blank=True)
    parent = models.ForeignKey('self', related_name='post_parent',
                               null=True, blank=True)
    author = models.ForeignKey(User, related_name="post_author",
                               null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=15, null=True, blank=True)
    type = models.CharField(max_length=25, blank=True, null=True)
    
    format = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    last_editor = models.ForeignKey(User,null=True, blank=True,
                                    related_name="post_last_editor",
                                    editable=False)
    last_date = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    objects = PostManager()
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        t = getattr(self, 'TYPE', None)
        if not self.type:
            self.type = t
        super(Post, self).save(*args, **kwargs)
    
    
    def add_comment(self, comment):
        if not isinstance(comment, Post):
            raise Exception('Post instance expected')
        comment.format = self.format
        comment.type = 'comment'
        comment.parent = self
        comment.save()
        
        if self.type == 'comment':
            var = self.postvar_post.get(key='post_reference')
            ref = var.value
        else:
            ref = self.id
        comment.postvar_post.create(key='reference', value=str(ref))
        
        comment.postvar_post.create(key='parent', value=str(self.id))
        for p in self.postvar_post.filter(key='parent'):
            comment.postvar_post.create(key='parent', value=p.value)
        
        return comment
    
    
    def find_comments(self):
        return self.post_parent.filter(type='comment')
    
    
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


class Comment(Post):
    TYPE = 'comment'
    
    class PaternityException(Exception):
        pass
    
    class Meta:
        proxy = True
    
    def save(self, *args, **kwargs):
        if not self.parent:
            err = "Orphan comment posts are not allowed"
            raise Comment.PaternityException(err)
        
        if not self.id: setref = True;
        else: setref = False;
        
        super(Comment, self).save(*args, **kwargs)
        
        # Setting references in first save
        if setref:
            parent = self.parent
            if not isinstance(parent, Comment):
                self._set_parents([self.parent_id])
                self._set_reference(self.parent_id)
            else:
                self._set_parents(parent.get_parents_bulk()\
                    .append(self.parent_id))
                self.set_reference(parent.get_reference())
    
    def get_parents_bulk(self):
        parents = self.postvar_post.filter(key='comment_parent')
        bulk = parents.values_list('value', flat=True)
        return bulk
    
    def get_reference(self):
        return self.postvar_post.get(key='comment_reference').value
    
    def _set_parents(self, parents):
        if not self.id:
            return False
        self.postvar_post.filter(key='comment_parent').delete()
        for parent in parents:
            self.postvar_post.create(key='comment_parent',
                                     value=str(parent))
        return True
    
    def _set_reference(self, parent_id):
        if not self.id:
            return False
        self.postvar_post.filter(key='comment_reference').delete()
        self.postvar_post.create(key='comment_reference', value=parent_id)
        return True
    
