from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags

from subjects.models import Tag
from resubmit.widgets import ResubmitFileWidget

from .models import PDFFile

class PDFFileForm(forms.ModelForm):
    subject = None
    MAX_UPLOAD_SIZE = 10*1024*1024

    def __init__(self, *args, **kwargs):
        super(PDFFileForm, self).__init__(*args, **kwargs)
        self.subject = kwargs.get('initial').get('subject', None)

        if self.instance.id:
            self.subject = self.instance.topic.subject
            self.initial['tags'] = ", ".join(self.instance.tags.all().values_list("name", flat = True))

        self.fields['students'].queryset = self.subject.students.all()
        self.fields['groups'].queryset = self.subject.group_subject.all()

    tags = forms.CharField(label = _('Tags'), required = False)
    class Meta:
        model = PDFFile
        fields = ['name', 'file', 'brief_description','show_window', 'all_students', 'students', 'groups', 'visible']
        labels = {
            'name': _('File name'),
        }
        widgets = {
            'brief_description': forms.Textarea,
            'students': forms.SelectMultiple,
            'groups': forms.SelectMultiple,
            'file': ResubmitFileWidget(attrs={'accept':'application/pdf, application/x-pdf, application/x-bzpdf, application/x-gzpdf'}),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '')

        topics = self.subject.topic_subject.all()

        for topic in topics:
            if self.instance.id:
                same_name = topic.resource_topic.filter(name__unaccent__iexact = name).exclude(id = self.instance.id).count()
            else:
                same_name = topic.resource_topic.filter(name__unaccent__iexact = name).count()

            if same_name > 0:
                self._errors['name'] = [_('This subject already has a pdf file with this name')]

                return ValueError

        return name

    def clean_file(self):
        file = self.cleaned_data.get('file', False)

        if file:
            if hasattr(file, '_size'):
                if file._size > self.MAX_UPLOAD_SIZE:
                    self._errors['file'] = [_("The file is too large. It should have less than 10MB.")]

                    return ValueError

        elif not self.instance.pk:
            self._errors['file'] = [_('This field is required.')]

            return ValueError

        return file

    def save(self, commit = True):
        super(PDFFileForm, self).save(commit = True)

        self.instance.save()

        previous_tags = self.instance.tags.all()

        tags = self.cleaned_data['tags'].split(",")

        #Excluding unwanted tags
        for prev in previous_tags:
            if not prev.name in tags:
                self.instance.tags.remove(prev)

        for tag in tags:
            tag = tag.strip()

            exist = Tag.objects.filter(name = tag).exists()

            if exist:
                new_tag = Tag.objects.get(name = tag)
            else:
                new_tag = Tag.objects.create(name = tag)

            if not new_tag in self.instance.tags.all():
                self.instance.tags.add(new_tag)

        return self.instance
