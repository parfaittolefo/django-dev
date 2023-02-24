from django import forms as forms #newforms
from django.forms import ModelForm
from .modelsapp import Publisher
TOPIC_CHOICES = (
('general', 'General enquiry'),
('bug', 'Bug report'),
('suggestion', 'Suggestion'),
)

class ContactForm(forms.Form):
    topic = forms.ChoiceField(choices=TOPIC_CHOICES)
    #message = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(),
    initial="Replace with your feedback")
    sender = forms.EmailField(required=False,label='Your e-mail address')

    def clean_message(self):
        message = self.cleaned_data['message']
        num_words = len(message.split(' '))
        if num_words < 4:
            raise forms.ValidationError("Not enough words!")
        return message

class PublisherForm(ModelForm):
    class Meta:
        model = Publisher
        fields = ['name','address','city','state_province','country','website']