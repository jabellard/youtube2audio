from django.db import models


class VideoManager(models.Manager):
    pass


class Video(models.Model):
    video_id = models.AutoField(
        primary_key=True,
    )
    youtube_id = models.CharField(
        null=False,
        unique=True,
        max_length=100,
    )
    last_downloaded = models.DateTimeField(
        null=True,
        default=None,
    )
    download_count = models.IntegerField(
        null=False,
        default=0
    )

    objects = VideoManager()

    def __str__(self):
        return '%s' % (self.youtube_id)

    def __unicode__(self):
        return '%s' % (self.youtube_id)

    class Meta:
        verbose_name = 'video'
