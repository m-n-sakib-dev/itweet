from django import forms
from .models import CommentModel

class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['content', 'parent']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Write your comment...',
                'class': 'form-control'
            }),
            'parent': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].required = False