from django.contrib import admin
from djazz.posts.models import Post, PostVar


class PostVarInline(admin.TabularInline):
    model = PostVar
    extra = 0


class PostAdmin(admin.ModelAdmin):
    inlines = [PostVarInline]
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.author = request.user
        obj.last_editor = request.user
        super(PostAdmin,self).save_model(request, obj, form, change)


admin.site.register(Post, PostAdmin)
