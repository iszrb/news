import xadmin
from app.models import *
from xadmin import views


class TypeAdmin(object):
    list_display = ['name']
    search_fields = ['name']
    list_filter =['name']

class ContentAdmin(object):
    list_display = ["id", "title", "picture"]
    search_fields = ["id", "publish_time", "title", "picture"]
    ordering = ["-publish_time"]
    list_per_page=2


class CommentAdmin(object):
    list_display = ["id", "content", "user_id", "news_id", "state"]
    search_fields = ["id", "publish_time", "user_id", "news_id"]
    list_editable = ["state"]
    ordering = ["-publish_time"]

#基础功能设置
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True
#全局设置
class GlobalSettings(object):
    # 后台管理系统的标题
    site_title = "后台管理系统"
    # 底部显示信息
    site_footer = "底部信息"
    # 折叠样式
    menu_style = "accordion"

xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(Type, TypeAdmin)
xadmin.site.register(Content, ContentAdmin)
xadmin.site.register(Comment, CommentAdmin)

