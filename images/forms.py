from django import forms

from albums.models import Album

class UploadFileForm(forms.Form):
    title = forms.CharField(required=True, label='Title')
    
    album = forms.ModelChoiceField(queryset=Album.objects.none(), initial=0)

    file = forms.FileField(required=True, label='Archivo')

    def __init__(self, queryset_album, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)

        self.fields['album'].queryset = queryset_album

        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['album'].widget.attrs['class'] = 'form-control'
        self.fields['file'].widget.attrs['class'] = 'form-control-file'