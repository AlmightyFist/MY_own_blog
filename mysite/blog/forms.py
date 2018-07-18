from django import forms
from .models import Post, Comment
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','body_text','tags',"category")

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget = forms.Textarea)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('body_text',)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput)
    password2 = forms.CharField(label = 'Powtórz hasło', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self): #metoda clean może zostać dostarczona dla dowolnego pola formularza w celu wyczyszczenia jego wartości lub zgłoszczenia błędu weryfikacji
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Hasła nie są identyczne.')

        return cd['password2']
