import django_filters
from apps.jobs.models import Job


class JobFilter(django_filters.FilterSet):

    min_salary = django_filters.NumberFilter(field_name="salary_min", lookup_expr="gte")
    max_salary = django_filters.NumberFilter(field_name="salary_max", lookup_expr="lte")
    experience = django_filters.NumberFilter(field_name="experience", lookup_expr="lte")

    class Meta:
        model = Job
        fields = [
            "job_type",
            "location",
        ]