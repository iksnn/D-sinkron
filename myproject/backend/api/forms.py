from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(
        label='Upload File Excel', 
        widget=forms.ClearableFileInput(attrs={'id': 'id_file', 'accept': '.xlsx'})
        )
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file.name.endswith('.xlsx'):
            raise forms.ValidationError('File harus berformat Excel.')
        return file