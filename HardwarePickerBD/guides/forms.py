from django import forms
from .models import Guides
from urllib.parse import urlparse, parse_qs

class GuidesForm(forms.ModelForm):
    class Meta:
        model = Guides
        fields = [
            'title',
            'image',
            'video_url',
            'cpu',
            'cpu_cooler',
            'motherboard',
            'memory',
            'storage',
            'gpu',
            'psu',
            'case',
        ]
        labels = {
            'image': 'Thumbnail Image',
            'video_url': 'YouTube Video URL',
        }
        help_texts = {
            'image': 'Optional thumbnail for homepage cards.',
            'video_url': 'Optional YouTube link for the guide page.',
        }

    def clean_video_url(self):
        url = self.cleaned_data.get('video_url')
        if url:
            parsed = urlparse(url)
            hostname = parsed.hostname or ''
            if not any(domain in hostname for domain in ['youtube.com', 'youtu.be']):
                raise forms.ValidationError("Only YouTube URLs are allowed.")
            vid = None
            if 'youtu.be' in hostname:
                vid = parsed.path.lstrip('/')
            elif 'youtube.com' in hostname:
                if parsed.path == '/watch':
                    vid = parse_qs(parsed.query).get('v', [None])[0]
                elif parsed.path.startswith('/embed/'):
                    vid = parsed.path.split('/')[2]
            if not vid:
                raise forms.ValidationError("Could not extract a valid video ID.")
        return url

    def clean(self):
        cleaned = super().clean()
        return cleaned
