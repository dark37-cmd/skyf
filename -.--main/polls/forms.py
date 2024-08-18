from django import forms
from .models import Question, Answer, UserDetail

class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super().__init__(*args, **kwargs)

        for question in questions:
            self.fields[f'question_{question.id}'] = forms.ModelChoiceField(
                queryset=question.answers.all(),
                widget=forms.RadioSelect,
                label=question.text,
                empty_label=None
            )


class UserDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['full_name', 'birth_date', 'skuf_type', 'photo']
