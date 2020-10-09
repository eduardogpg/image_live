from django import forms

DEMO = [
    (1, 'Demo'),
    (2, 'Demo2'),
]

# forms.Model
class UploadFileForm(forms.Form):
    title = forms.CharField(required=True, label='Title')
    album = forms.ChoiceField(choices=DEMO, label='Album')
    file = forms.FileField(required=True, label='Archivo')

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['album'].widget.attrs['class'] = 'form-control'
        self.fields['file'].widget.attrs['class'] = 'form-control-file'