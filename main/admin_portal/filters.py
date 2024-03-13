import django_filters
from django import forms
from .models import Students

class studentfilter(django_filters.FilterSet):
   # name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Students
        fields = {'roll_number': ['icontains'],
                  'name': ['icontains'],
                  'course': ['icontains'],
                  'category': ['icontains'],
                  'department': ['icontains'],
                  }
        # filter_overrides = {
        #      Students.CharField: {
        #          'filter_class': django_filters.CharFilter,
        #          'extra': lambda f: {
        #              'lookup_expr': 'icontains',
        #              'widget': studentfilter.form.TextInput(attrs={'class': 'form-control'})
        #          },
        #      }
        # }
        