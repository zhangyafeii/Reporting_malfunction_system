from django.db import models
from tinymce.models import HTMLField


class UserInfo(models.Model):
    """
    用户信息表
    """
    username = models.CharField(max_length=32,verbose_name='用户名',unique=True)
    pwd = models.CharField(max_length=16,verbose_name='密码')
    nickname = models.CharField(max_length=32,verbose_name='昵称',unique=True)
    email = models.EmailField(verbose_name='邮箱',unique=True)
    img = models.ImageField(verbose_name='图片',upload_to='static/upload/photo')
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)

    fans = models.ManyToManyField(verbose_name='粉丝们',to='UserInfo',through='Fans',related_name='f',through_fields=('user','fan'))

    class Meta:
        verbose_name_plural = '用户信息'

    def __str__(self):
        return self.username


class Blog(models.Model):
    """
    个人博客信息表
    """
    suffix = models.CharField(max_length=32,verbose_name='主站名称',unique=True)
    theme = models.CharField(max_length=32,verbose_name='博客主题',default='warm')
    title = models.CharField(max_length=32,verbose_name='个人博客标题')
    summary = models.CharField(max_length=32,verbose_name='博客简介')

    user = models.OneToOneField('UserInfo',on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '博客表'

    def __str__(self):
        return self.suffix


class Fans(models.Model):
    """
    粉丝表
    """
    user = models.ForeignKey('UserInfo',related_name='users',on_delete=models.CASCADE)
    fan = models.ForeignKey('UserInfo',on_delete=models.CASCADE,related_name='fan')

    class Meta:
        verbose_name_plural = '互粉表'


class Classification(models.Model):
    """
    个人博客文章分类表
    """
    title = models.CharField(max_length=32,verbose_name='分类标题')
    blog = models.ForeignKey('Blog',verbose_name='所属博客',related_name='classification',on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '分类'

    def __str__(self):
        return self.title


class Tags(models.Model):
    """
    个人博客文章标签表
    """
    title = models.CharField(max_length=32)
    blog = models.ForeignKey('Blog',on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '标签'

    def __str__(self):
        return self.title


class Article(models.Model):
    """
    文章信息表
    """
    title = models.CharField(max_length=32,verbose_name='标题')
    summary = models.CharField(max_length=128,verbose_name='概述')
    detail = HTMLField(verbose_name='正文')
    create_time = models.DateTimeField(verbose_name='创建时间',auto_now_add=True)
    read_count = models.IntegerField(default=0,verbose_name='阅读次数')
    up_count = models.IntegerField(default=0,verbose_name='点赞次数')
    down_count = models.IntegerField(default=0,verbose_name='踩次数')
    comment_count = models.IntegerField(default=0,verbose_name='评论次数')
    img = models.ImageField(verbose_name='文章封面',upload_to='static/upload/artcle',null=True)
    blog = models.ForeignKey(to='Blog',verbose_name='所属博客',on_delete=models.CASCADE,related_name='article')
    article_classification = models.ForeignKey('Classification',verbose_name='个人博客文章分类',on_delete=models.SET_NULL,null=True,related_name='classification')
    publish_choices = (
        (0,'未发布'),
        (1,'已发布'),
    )
    publish = models.IntegerField(choices=publish_choices,default=0)

    type_choices = [(1,'Python全栈'),(2,'大数据'),(3,'WEB开发'),(4,'前端与移动开发'),(5,'运维'),(6,'数据库')]

    article_type_id = models.IntegerField(choices=type_choices,default=None,verbose_name='文章类型')

    tags = models.ManyToManyField(to='Tags',through='Ariticle_Tags',through_fields=('article','tag'))

    class Meta:
        verbose_name_plural = '文章'

    def __str__(self):
        return self.title


class Ariticle_Tags(models.Model):
    """
    文章标签表
    """
    article = models.ForeignKey('Article',on_delete=models.CASCADE)
    tag = models.ForeignKey('Tags',on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '文章标签'


class Article_like_dislike(models.Model):
    """
    文章点赞表
    """
    article = models.ForeignKey('Article',on_delete=models.CASCADE,related_name='likes')
    user = models.ForeignKey('UserInfo',on_delete=models.CASCADE,related_name='likes')
    like = models.BooleanField(verbose_name='是否赞')

    #ManyToManyField字段默认生成联合唯一
    class Meta:
        verbose_name_plural = '文章点赞或踩'
        unique_together = [('article','user')]


class Comment(models.Model):
    """
    评论表
    """
    content = models.CharField(max_length=128,verbose_name='评论')
    article = models.ForeignKey('Article',on_delete=models.CASCADE,verbose_name='评论文章',related_name='comment')
    comment_user = models.ForeignKey('UserInfo',on_delete=models.CASCADE,verbose_name='评论者')
    comment_time = models.DateTimeField(auto_now_add=True,verbose_name='评论时间')
    parent_id = models.ForeignKey(to='self',on_delete=models.CASCADE,blank=True,null=True)

    class Meta:
        verbose_name_plural = '评论表'


class Trouble(models.Model):
    """
    报障单
    """
    title = models.CharField(max_length=32)
    detail = models.TextField()
    user = models.ForeignKey(to='UserInfo',related_name='u',on_delete=models.CASCADE)
    # ctime = models.CharField(max_length=32)
    ctime = models.DateTimeField()
    status_choices=(
        (1,'未处理'),
        (2,'处理中'),
        (3,'已处理'),
    )
    status = models.IntegerField(choices=status_choices,default=1)

    processor = models.ForeignKey(UserInfo,related_name='p',null=True,blank=True,on_delete=models.SET_NULL)
    solution = models.TextField(null=True,blank=True)
    ptime = models.DateTimeField(null=True,blank=True)

    evaluate_choices = (
        (1, '不满意'),
        (2, '一般'),
        (3, '活很好'),
    )
    evaluate = models.IntegerField(choices=evaluate_choices,null=True,blank=True)

    class Meta:
        verbose_name_plural = '报障单'

    def __str__(self):
        return self.title


class TroubleTemplate(models.Model):
    """
    报障单模板表
    """
    title = models.CharField(max_length=32)
    context = models.TextField()
    user = models.ForeignKey('UserInfo',on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '报障单模板'

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色表
    """
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural='角色表'

    def __str__(self):
        return self.name


class UserinfoToRole(models.Model):
    """
    用户和角色之间是多对多关系
    """
    user = models.ForeignKey(to='UserInfo',on_delete=models.CASCADE)
    role = models.ForeignKey(to='Role',on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='用户分配角色表'

    def __str__(self):
        return '{}-{}'.format(self.user.username,self.role.name)


class Action(models.Model):
    """
    每个url地址中的具体操作权限
    ?get        查询
    ?post       增
    ?put        改
    ?delete     删
    """
    caption = models.CharField(max_length=32)
    code = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural='操作表'

    def __str__(self):
        return self.caption


class Permission(models.Model):
    """
    url地址权限
    """

    caption = models.CharField(max_length=32)
    url = models.CharField(max_length=128)
    menu = models.ForeignKey('Menu',null=True,blank=True,on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural='URL表'

    def __str__(self):
        return '{}-{}'.format(self.caption,self.url)


class PermissionToAction(models.Model):
    """
    url权限与具体操作权限多对多关系
    """
    permission = models.ForeignKey(to='Permission',on_delete=models.CASCADE)
    action = models.ForeignKey(to='Action',on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='权限表'

    def __str__(self):
        return '{}-{}:{}?t={}'.format(self.permission.caption,self.action.caption,self.permission.url,self.action.code)


class RoleToPremissionToAction(models.Model):
    """
    角色与权限是多对多关系
    """
    role = models.ForeignKey(to='Role',on_delete=models.CASCADE)
    p2a = models.ForeignKey(to='PermissionToAction',on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='角色分配权限'

    def __str__(self):
        return '{}-{}'.format(self.role.name,self.p2a)


class Menu(models.Model):
    """
    1   菜单1     null
    2   菜单2     null
    3   菜单3     null
    4   菜单1.1    1
    5   菜单1.2    1
    6   菜单1.2.1  4
    无最后一层
    """
    caption = models.CharField(max_length=32)
    parent = models.ForeignKey('self',related_name='p',null=True,blank=True,on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural='菜单表'

    def __str__(self):
        return self.caption

