from django.contrib import admin
from repository.models import *

admin.site.register(UserInfo)
admin.site.register(Blog)
admin.site.register(Fans)
admin.site.register(Classification)
admin.site.register(Tags)
admin.site.register(Article)
admin.site.register(Ariticle_Tags)
admin.site.register(Article_like_dislike)
admin.site.register(Comment)
admin.site.register(Trouble)
admin.site.register(TroubleTemplate)
admin.site.register(Role)
admin.site.register(UserinfoToRole)
admin.site.register(Permission)
admin.site.register(Action)
admin.site.register(PermissionToAction)
admin.site.register(RoleToPremissionToAction)
admin.site.register(Menu)
