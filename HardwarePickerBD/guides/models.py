from django.db import models
from urllib.parse import urlparse, parse_qs

class Guides(models.Model):
    image = models.ImageField(upload_to='guide_images/', null=True, blank=True)
    title = models.CharField(max_length=200)
    cpu = models.TextField()
    cpu_cooler = models.TextField()
    motherboard = models.TextField()
    memory = models.TextField()
    storage = models.TextField()
    gpu = models.TextField()
    psu = models.TextField()
    case = models.TextField()
    video_url = models.URLField(null=True, blank=True)

    def get_video_id(self):
        """Extract YouTube video ID from URL"""
        if self.video_url:
            parsed_url = urlparse(self.video_url)
            if parsed_url.hostname in ['youtu.be', 'www.youtu.be']:
                return parsed_url.path[1:]
            if parsed_url.hostname in ['youtube.com', 'www.youtube.com']:
                if parsed_url.path == '/watch':
                    return parse_qs(parsed_url.query).get('v', [None])[0]
                if parsed_url.path.startswith('/embed/'):
                    return parsed_url.path.split('/')[2]
        return None

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "View Guides"

class GuidesImages(models.Model):
    guide = models.ForeignKey(Guides, on_delete=models.CASCADE, related_name='images')
    component = models.CharField(max_length=50, choices=[
        ('CPU', 'CPU'),
        ('CPU Cooler', 'CPU Cooler'),
        ('Motherboard', 'Motherboard'),
        ('Memory', 'Memory'),
        ('Storage', 'Storage'),
        ('GPU', 'GPU'),
        ('PSU', 'PSU'),
        ('Case', 'Case'),
    ])
    image = models.ImageField(upload_to='guides/images/')

    def __str__(self):
        return f"{self.component} Image for {self.guide.title}"
