from django import forms

from albums.models import Album

class UploadFileForm(forms.Form):
    # title = forms.CharField(required=True, label='Title')
    # album = forms.ModelChoiceField(queryset=Album.objects.none(), initial=0)
    
    album_id = forms.CharField(required=True, widget=forms.HiddenInput())
    file = forms.FileField(required=True, label='Archivo',
                            widget=forms.FileInput(attrs={'accept':'image/*'}))

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)

        # self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['file'].widget.attrs['class'] = 'form-control-file'