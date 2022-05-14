from django import forms

class AddPostForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={"rows":"2"}))

    def __init__(self, *args, **kwargs):
        super(AddPostForm, self).__init__(*args, **kwargs)
        # add a "form-control" class to each form input
        # for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })
