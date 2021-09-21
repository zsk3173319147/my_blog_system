from functools import cached_property
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import markdown
from django.utils.html import strip_tags
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
import re
# Create your models here.
  
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) :
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    # 文章标题
    title = models.CharField(max_length=70)

    # 文章正文 使用 textfield 类型
    body = models.TextField()

    # 这两列分别表示文章的创建时间和最后一次修改时间 存储时间的字段用 DateTimeField 类型
    created_time = models.DateTimeField(default=timezone.now())
    modified_time = models.DateTimeField()

    # 文章摘要 可以没有但是默认情况下 charfield 要求我们输入数据
    excerpt = models.CharField(max_length=200, blank=True)

    # 这里是分类和标签
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)

    # 文章的作者
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 新增views字段记录阅读量
    views=models.PositiveIntegerField(default=0,editable=False)

    @property
    def toc(self):
        return self.rich_content.get("toc", "")

    @property
    def body_html(self):
        return self.rich_content.get("content", "")

    @cached_property
    def rich_content(self):
        return generate_rich_content(self.body)

    def __str__(self):
        return self.title
    
    # 自定义get_abslute_url方法
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})
    
    def save(self,*args,**kwargs):
        self.modified_time = timezone.now()

        # 首先实例化一个 Markdown 类，用于渲染 body 的文本。
        # 由于摘要并不需要生成文章目录，所以去掉了目录拓展。
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        # 先将 Markdown 文本渲染成 HTML 文本
        # strip_tags 去掉 HTML 文本的全部 HTML 标签
        # 从文本摘取前 54 个字符赋给 excerpt
        if not self.excerpt.strip():
            self.excerpt = strip_tags(md.convert(self.body))[:200]

        super().save(*args, **kwargs)
    
    def increase_views(self):
        self.views+=1
        self.save(update_fields=['views'])
    
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = 'verbose_name'
        ordering=['-created_time']
    

def generate_rich_content(value):
    md = markdown.Markdown(
        extensions=[
            "markdown.extensions.extra",
            "markdown.extensions.codehilite",
            # 记得在顶部引入 TocExtension 和 slugify
            TocExtension(slugify=slugify),
        ]
    )
    content = md.convert(value)
    m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
    toc = m.group(1) if m is not None else ""
    return {"content": content, "toc": toc}


