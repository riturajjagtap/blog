from django import forms
from blogapp.models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author', 'title', 'written_text')

        widgets = {
            'title':forms.TextInput(attrs={'class':'textinputclass',
                                            'autofocus':'autofocus'}),
            'written_text':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent',
                                            'autofocus':'autofocus'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author','comment_text')

        widgets = {
            'author':forms.TextInput(attrs={'class':'textinputclass'}),
            'comment_text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'}),
        }
