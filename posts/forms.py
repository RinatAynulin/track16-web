from django import forms

from posts.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'url', 'description')

class SearchForm(forms.Form):
    q = forms.CharField(max_length=100)

class OrderByForm(forms.Form):
    CHOICES = (('-created_at', u'Publication time'), ('green', u'rating'))
    order = forms.ChoiceField(choices=CHOICES, label=u'Order by')