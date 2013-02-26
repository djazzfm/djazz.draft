from django import forms
from djazz.posts.models import Comment


class CommentForm(forms.ModelForm):
    type = forms.CharField(widget=forms.HiddenInput, initial='comment')
    format = forms.CharField(widget=forms.HiddenInput, initial='default', required=False)
    content = forms.CharField(widget=forms.Textarea, required=True)
    
    class Meta:
        model = Comment
        widgets = {
            'title': forms.HiddenInput(),
            'parent': forms.HiddenInput(),
            'author': forms.HiddenInput(),
            'lang': forms.HiddenInput(),
            'status': forms.HiddenInput()
        }
    
class CommentAnonymousForm(CommentForm):
    
    author_name = forms.CharField()
    author_email = forms.EmailField()
    
    def save(self, *args, **kwargs):
        c = super(CommentAnonymousForm, self).save(*args, **kwargs)
        author = c.postvar_post.get_or_create(key='comment_author')[0]
        author.value = self.cleaned_data['author_name']
        author.save()
