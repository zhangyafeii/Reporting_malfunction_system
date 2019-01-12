# Generated by Django 2.0.5 on 2018-09-25 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ariticle_Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': '文章标签',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('summary', models.CharField(max_length=128, verbose_name='概述')),
                ('detail', models.TextField(verbose_name='正文')),
                ('create_time', models.DateTimeField(verbose_name='创建时间')),
                ('read_count', models.IntegerField(default=0)),
                ('article_type_id', models.IntegerField(choices=[(1, 'Python'), (2, 'javascript'), (3, 'openstacks'), (4, 'linux'), (5, 'php')], default=None)),
            ],
            options={
                'verbose_name_plural': '文章',
            },
        ),
        migrations.CreateModel(
            name='Article_like_dislike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(verbose_name='是否赞')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Article')),
            ],
            options={
                'verbose_name_plural': '文章点赞或踩',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suffix', models.CharField(max_length=32, verbose_name='主站名称')),
                ('theme', models.CharField(max_length=32, verbose_name='博客主题')),
                ('title', models.CharField(max_length=32, verbose_name='个人博客标题')),
                ('summary', models.CharField(max_length=32, verbose_name='博客简介')),
            ],
            options={
                'verbose_name_plural': '博客表',
            },
        ),
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='分类标题')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog', to='repository.Blog', verbose_name='所属博客')),
            ],
            options={
                'verbose_name_plural': '分类',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=128, verbose_name='评论')),
                ('comment_time', models.DateTimeField(auto_now_add=True, verbose_name='评论时间')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Article', verbose_name='评论文章')),
            ],
            options={
                'verbose_name_plural': '评论表',
            },
        ),
        migrations.CreateModel(
            name='Fans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': '互粉表',
            },
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Blog')),
            ],
            options={
                'verbose_name_plural': '标签',
            },
        ),
        migrations.CreateModel(
            name='TroubleTicket',
            fields=[
                ('uuid', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64, verbose_name='故障标题')),
                ('detail', models.CharField(max_length=256, verbose_name='故障详情')),
                ('status', models.CharField(choices=[(1, '待处理'), (2, '处理中'), (3, '已处理')], max_length=32, verbose_name='处理状态')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('resolve_time', models.DateTimeField(verbose_name='处理时间')),
            ],
            options={
                'verbose_name_plural': '报障表',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True, verbose_name='用户名')),
                ('pwd', models.CharField(max_length=64, verbose_name='密码')),
                ('nickname', models.CharField(max_length=32, verbose_name='昵称')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('img', models.ImageField(max_length=32, upload_to='static/upload/photo', verbose_name='图片')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('fans', models.ManyToManyField(related_name='f', through='repository.Fans', to='repository.UserInfo', verbose_name='粉丝们')),
            ],
            options={
                'verbose_name_plural': '用户信息',
            },
        ),
        migrations.AddField(
            model_name='troubleticket',
            name='ask_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ask_user', to='repository.UserInfo'),
        ),
        migrations.AddField(
            model_name='troubleticket',
            name='processor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='processor', to='repository.UserInfo'),
        ),
        migrations.AddField(
            model_name='fans',
            name='fan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fan', to='repository.UserInfo'),
        ),
        migrations.AddField(
            model_name='fans',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users', to='repository.UserInfo'),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.UserInfo', verbose_name='评论者'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.Comment'),
        ),
        migrations.AddField(
            model_name='blog',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='repository.UserInfo'),
        ),
        migrations.AddField(
            model_name='article_like_dislike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.UserInfo'),
        ),
        migrations.AddField(
            model_name='article',
            name='article_classification',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='repository.Classification'),
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.UserInfo', verbose_name='作者'),
        ),
        migrations.AddField(
            model_name='article',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Blog', verbose_name='所属博客'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(through='repository.Ariticle_Tags', to='repository.Tags'),
        ),
        migrations.AddField(
            model_name='ariticle_tags',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Article'),
        ),
        migrations.AddField(
            model_name='ariticle_tags',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.Tags'),
        ),
        migrations.AlterUniqueTogether(
            name='article_like_dislike',
            unique_together={('article', 'user')},
        ),
    ]