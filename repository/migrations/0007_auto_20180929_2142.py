# Generated by Django 2.0.5 on 2018-09-29 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0006_auto_20180927_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_classification',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='classification', to='repository.Classification', verbose_name='个人博客文章分类'),
        ),
        migrations.AlterField(
            model_name='article',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article', to='repository.Blog', verbose_name='所属博客'),
        ),
        migrations.AlterField(
            model_name='article_like_dislike',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='repository.Article'),
        ),
        migrations.AlterField(
            model_name='article_like_dislike',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='repository.UserInfo'),
        ),
        migrations.AlterField(
            model_name='classification',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classification', to='repository.Blog', verbose_name='所属博客'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='repository.Article', verbose_name='评论文章'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.Comment'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='nickname',
            field=models.CharField(max_length=32, unique=True, verbose_name='昵称'),
        ),
    ]
