from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill
from django.core.validators import FileExtensionValidator
# Create your models here.

class post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    pub_date = models.DateField(auto_now=True)


    def recent(self):
        dl = datetime.today().date() - timedelta(days=2)
        chk = self.pub_date
        if chk < dl:
            return False
        else:
            return True

    def __str__(self):
        return str(self.author) + str(self.title)


class user_image(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="avatars")
    image_medium = ImageSpecField(source="image",processors=[ResizeToFill(165,165)],format='JPEG',options={'quality':100})


class post_image(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images")
    image_medium = ImageSpecField(source="image",processors=[ResizeToFill(640,333)],format='JPEG',options={'quality':100})
    image_max = ImageSpecField(source="image",processors=[ResizeToFill(1920,1080)],format='JPEG',options={'quality':100})

class post_comment(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return str(self.post) + str(self.author)



class subscription(models.Model):
    subscriber = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sub')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author')

    def __str__(self):
        return str(self.subscriber) + " -> " + str(self.author)


class post_video(models.Model):
    post = models.ForeignKey(post,on_delete=models.CASCADE)
    video = models.FileField(upload_to="videos",validators=[FileExtensionValidator(allowed_extensions=['ogg','mp4','webm'])])


class user_name(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

class user_donate_link(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    link = models.URLField(max_length=400)

class user_premium(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class post_attached_link(models.Model):
    post = models.ForeignKey(post,on_delete=models.CASCADE)
    url = models.URLField(max_length=400)

class reply(models.Model):
    parent_comment = models.ForeignKey(post_comment,on_delete=models.CASCADE,blank=True, null=True)
    parent_reply = models.ForeignKey("self",on_delete=models.CASCADE,blank=True, null=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField()


class report_reason(models.Model):
    reason = models.CharField(max_length=150)

    def __str__(self):
        return self.reason


class report(models.Model):
    post = models.ForeignKey(post,on_delete=models.CASCADE,blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    reason = models.CharField(max_length=150)
    details = models.TextField()

    def __str__(self):
        if self.post:
            return str(self.post) + " "+ str(self.reason)
        else :
            return str(self.user) + " "+ str(self.reason)
