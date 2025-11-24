from django import forms
from .models import CommentModel

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['content', 'parent']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Write your comment...',
                'class': 'form-content-area container'
            }),
            'parent': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].required = False