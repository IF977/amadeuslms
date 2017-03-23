from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.translation import ugettext_lazy as _

from django import forms
from django.core.urlresolvers import reverse_lazy

from django.contrib import messages

import django.views.generic as generic
from mural.models import SubjectPost, Comment, MuralVisualizations
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, date, timedelta
from subjects.models import Subject, Tag
from .forms import CreateInteractionReportForm, ResourceAndTagForm, BaseResourceAndTagFormset
from log.models import Log
from topics.models import Resource, Topic
from collections import OrderedDict
from django.forms import formset_factory
from .models import ReportCSV, ReportXLS
import pandas as pd

class ReportView(LoginRequiredMixin, generic.FormView):
    template_name = "reports/create.html"
    form_class = CreateInteractionReportForm
    
    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.
        """

        initial = {}
        params = self.request.GET
        subject = Subject.objects.get(id=params['subject_id'])
        topics = subject.topic_subject.all()
        initial['subject'] = subject
        initial['topic'] = topics
        initial['end_date'] =  date.today()
        return initial

    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        subject = Subject.objects.get(id=self.request.GET['subject_id'])

        context['subject'] = subject

        topics = subject.topic_subject.all()
        #get all resources associated with topics
        tags = []
        for topic in topics:
            resources_set = topic.resource_topic.all()
            for resource in resources_set:
                for tag in resource.tags.all():
                    tags.append(tag)
        

        classes = Resource.__subclasses__()    


        #set formset
        resourceTagFormSet = formset_factory(ResourceAndTagForm, formset=BaseResourceAndTagFormset)
        resourceTagFormSet = resourceTagFormSet()
        context['resource_tag_formset'] = resourceTagFormSet
        return context

    def get_success_url(self):

        messages.success(self.request, _("Report created successfully"))

        get_params = "?"
        #passing form data through GET 
        for key, value in self.form_data.items():
            get_params += key +  "=" + str(value)  + "&"

        
        for form_data in self.formset_data:   
            for key, value in form_data.items():
                get_params += key +  "=" + str(value)  + "&"

        #retrieving subject id for data purposes
        for key, value in self.request.GET.items():
            get_params += key + "=" + str(value) 

        return reverse_lazy('subjects:reports:view_report', kwargs={}) + get_params

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form = self.get_form()

        subject = Subject.objects.get(id=self.request.GET['subject_id'])

        topics = subject.topic_subject.all()
        #get all resources associated with topics
        tags = []
        for topic in topics:
            resources_set = topic.resource_topic.all()
            for resource in resources_set:
                for tag in resource.tags.all():
                    tags.append(tag)

        classes = Resource.__subclasses__()  
        amount_of_forms = self.request.POST['form-TOTAL_FORMS']
        initial_datum = {'class_name': classes , 'tag': tags}
        initial_data = []
        for i in range(int(amount_of_forms)):
            initial_data.append(initial_datum)

        resourceTagFormSet = formset_factory(ResourceAndTagForm, formset=BaseResourceAndTagFormset)
        resources_formset = resourceTagFormSet(self.request.POST, initial = initial_data)
        if form.is_valid() and resources_formset.is_valid():
            self.form_data = form.cleaned_data
            self.formset_data = resources_formset.cleaned_data
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ViewReportView(LoginRequiredMixin, generic.TemplateView):
    template_name = "reports/view.html"


    def get_context_data(self, **kwargs):
        context = {}
        params_data = self.request.GET
        subject = Subject.objects.get(id=params_data['subject_id'])
        context['subject_name'] = subject.name
        context['topic_name'] = params_data['topic']
        context['init_date'] = params_data['init_date']
        context['end_date'] = params_data['end_date']
        context['subject'] = subject
      
        #I used getlist method so it can get more than one tag and one resource class_name
        resources = params_data.getlist('resource')
        tags = params_data.getlist('tag')
        
        self.from_mural = params_data['from_mural']
       
        context['data'], context['header'] = self.get_mural_data(subject, params_data['init_date'], params_data['end_date'],
            resources, tags )


        #this is to save the csv for further download
        df = pd.DataFrame.from_dict(context['data'], orient='index')
        df.columns = context['header']
        #so it does not exist more than one report CSV available for that user to download
        if ReportCSV.objects.filter(user= self.request.user).count() > 0:
            report = ReportCSV.objects.get(user=self.request.user)
            report.delete()
      
        
        report = ReportCSV(user= self.request.user, csv_data = df.to_csv())
        report.save()

        #for excel files
        """ if ReportXLS.objects.filter(user= self.request.user).count() > 0:
            report = ReportXLS.objects.get(user=self.request.user)
            report.delete()
        
        df.drop(df.columns[[0]], axis=1, inplace=True)
        writer = pd.ExcelWriter('pandas_simple.xlsx')
        report = ReportXLS(user= self.request.user, xls_data = df.to_excel(writer))
        report.save()"""


        return context

    def get_mural_data(self, subject, init_date, end_date, resources_id, tags_id):
        data = {}
        students = subject.students.all()
        formats = ["%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d"] #so it accepts english and portuguese date formats
        for fmt in formats:
            try:
                init_date = datetime.strptime(init_date, fmt).date()
                end_date = datetime.strptime(end_date, fmt).date()
                
            except ValueError:
                pass

        header = ['User']
       
        #I use this so the system can gather data up to end_date 11h59 p.m.
        end_date = end_date + timedelta(days=1)
   
       
        #For each student in the subject
        for student in students:
            data[student] = []

            data[student].append(student.social_name)

            interactions = OrderedDict()    
                  
            #interactions['username'] = student.social_name
            if self.from_mural == "True":
                help_posts_made_by_user = SubjectPost.objects.filter(action="help",space__id=subject.id, user=student, 
                    create_date__range=(init_date, end_date))

                #number of help posts created by the student
                interactions[_('Number of help posts created by the user.')] = help_posts_made_by_user.count()

                help_posts = SubjectPost.objects.filter(action="help", create_date__range=(init_date, end_date), 
                space__id=subject.id)

                #comments count on help posts created by the student
                interactions[_('Amount of comments on help posts created by the student.')] = Comment.objects.filter(post__in = help_posts.filter(user=student), 
                    create_date__range=(init_date, end_date)).count()
                

                #count the amount of comments made by the student on posts made by one of the professors
                interactions[_('Amount of comments made by the student on teachers help posts.')] = Comment.objects.filter(post__in = help_posts.filter(user__in= subject.professor.all()), create_date__range=(init_date, end_date),
                 user=student).count()

                 #comments made by the user on other users posts
                interactions[_('Amount of comments made by the student on other students help posts.')] = Comment.objects.filter(post__in = help_posts.exclude(user=student), 
                    create_date__range=(init_date, end_date),
                    user= student).count()
               
                
                
                comments_by_teacher = Comment.objects.filter(user__in=subject.professor.all())
                help_posts_ids = []
                for comment in  comments_by_teacher:
                    help_posts_ids.append(comment.post.id)
                 #number of help posts created by the user that the teacher commented on
                interactions[_('Number of help posts created by the user that the teacher commented on.')] = help_posts.filter(user=student, id__in = help_posts_ids).count()

               
                comments_by_others = Comment.objects.filter(user__in=subject.students.exclude(id = student.id))
                help_posts_ids = []
                for comment in  comments_by_teacher:
                    help_posts_ids.append(comment.post.id)
                #number of help posts created by the user others students commented on
                interactions[_('Number of help posts created by the user others students commented on.')] = help_posts.filter(user=student, id__in = help_posts_ids).count()

                #Number of student visualizations on the mural of the subject
                interactions[_('Number of student visualizations on the mural of the subject.')] = MuralVisualizations.objects.filter(post__in = SubjectPost.objects.filter(space__id=subject.id),
                    user = student).count()
            

            #VAR08 through VAR_019 of documenttation:
            if len(resources_id) > 0:
                resources_data = self.get_resources_and_tags_data(resources_id, tags_id, student, subject, init_date, end_date)
                for key, value in resources_data.items():
                    interactions[key] = value


            #VAR20 - number of access to mural between 6 a.m to 12a.m.
            interactions[_('Number of access to mural between 6 a.m to 12a.m. .')] =  Log.objects.filter(action="access", resource="subject", 
                user_id= student.id, context__contains = {'subject_id' : subject.id}, datetime__hour__range = (5, 11),  datetime__range=(init_date,end_date)).count()

            #VAR21 - number of access to mural between 0 p.m to 6p.m.
            interactions[_('Number of access to mural between 0 p.m to 6p.m. .')] =  Log.objects.filter(action="access", resource="subject", 
                user_id= student.id, context__contains = {'subject_id' : subject.id}, datetime__hour__range = (11, 17), datetime__range=(init_date,end_date)).count()
            #VAR22
            interactions[_('Number of access to mural between 6 p.m to 12p.m. .')] =  Log.objects.filter(action="access", resource="subject", 
                user_id= student.id, context__contains = {'subject_id' : subject.id}, datetime__hour__range = (17, 23),  datetime__range=(init_date,end_date)).count()

            #VAR23
            interactions[_('Number of access to mural between 0 a.m to 6a.m. .')] =  Log.objects.filter(action="access", resource="subject", 
                user_id= student.id, context__contains = {'subject_id' : subject.id}, datetime__hour__range = (23, 5),  datetime__range=(init_date,end_date)).count()

            #VAR24 through 30
            day_numbers = [0, 1, 2, 3, 4, 5, 6]
            day_names = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
            distinct_days = 0
            for day_num in day_numbers:
                interactions[_('Number of access to the subject on ')+ day_names[day_num]] =  Log.objects.filter(action="access", resource="subject", 
                user_id= student.id, context__contains = {'subject_id' : subject.id}, datetime__week_day = day_num, datetime__range = (init_date, end_date)).count()
                #to save the distinct days the user has accessed 
                if interactions[_('Number of access to the subject on ')+ day_names[day_num]] > 0:
                    distinct_days += 1

            interactions[_('Number of distinct days the user access the subject. ')] = distinct_days
            interactions[_("Class")] = ""
            interactions[_("Performance")] = ""
            for value in interactions.values():
                data[student].append(value)
           
                
        for key in interactions.keys():
            header.append(key)
        return data, header

    def get_resources_and_tags_data(self, resources_types, tags, student, subject, init_date, end_date):
        data = OrderedDict()  
        print(tags)
        for i in range(len(resources_types)):
            
            resources = Resource.objects.select_related(resources_types[i].lower()).filter(tags__in = tags, topic__in=subject.topic_subject.all())
            distinct_resources = 0
            total_count = 0
            for resource in resources:
                count = Log.objects.filter(action="view", resource=resources_types[i].lower(),
                      user_id = student.id, context__contains = {'subject_id': subject.id, 
                      resources_types[i].lower()+'_id': resource.id}, datetime__range=(init_date, end_date)).count()
                if count > 0:
                    distinct_resources += 1
                    total_count += count
                
            data[str(resources_types[i]) + " with tag " + Tag.objects.get(id=int(tags[i])).name] = total_count
            data["distintic " + str(resources_types[i]) + " with tag " + Tag.objects.get(id=int(tags[i])).name] = distinct_resources
            """data["distinct" + str(resources[i]) + " with tag " + Tag.objects.get(id=int(tags[i])).name] = Log.objects.filter(action="view", resource=resources[i].lower(),
                user_id = student.id, context__contains = {'subject_id': subject.id}).distinct().count()"""

        return data


"""
Get all possible resource subclasses available for that topic selected
"""
def get_resources(request):

    #get all possible resources
    classes = Resource.__subclasses__()    

    data = {}
    subject = Subject.objects.get(id=request.GET['subject_id'])

    topic_choice = request.GET["topic_choice"]
    if topic_choice.lower() == "all" or topic_choice.lower() == "todos":
        topics = subject.topic_subject.all()
    else:
        topics = [Topic.objects.get(id=int(topic_choice))]

    resources_class_names = []
    for topic in topics:
        resource_set = Resource.objects.filter(topic = topic)
        for resource in resource_set:
            resources_class_names.append(resource._my_subclass)

    #remove duplicates
    resources = set(resources_class_names)

    data['resources']= [ {'id':resource_type, 'name':resource_type} for resource_type in  resources]
    return JsonResponse(data)



"""
This function returns all the tags associated 
with a resource that is of the type of of the resource_class_name provided.
"""
def get_tags(request):
    resource_type = request.GET['resource_class_name']
    subject = Subject.objects.get(id=request.GET['subject_id'])
    topic_choice = request.GET["topic_choice"]
    
    #Have to fix this to accept translated options
    if topic_choice.lower() == "all" or topic_choice.lower() == "todos":
        topics = subject.topic_subject.all()
    else:
        topics = [Topic.objects.get(id=int(topic_choice))]
    data = {}
    tags = set()
    for topic in topics:
        resource_set = Resource.objects.select_related(resource_type.lower()).filter(topic = topic)
       
        for resource in resource_set:
            if resource._my_subclass == resource_type.lower():
                for tag in resource.tags.all():
                    if tag.name != "":
                        tags.add(tag)
                
   
    #adding empty tag for the purpose of giving the user this option for adicional behavior
    tags = list(tags)
    tags.append(Tag(name=""))
    data['tags'] = [ {'id':tag.id, 'name':tag.name} for tag in  tags]
    return JsonResponse(data)


def download_report_csv(request):
    report = ReportCSV.objects.get(user=request.user)
     
    response = HttpResponse(report.csv_data,content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'

    return response