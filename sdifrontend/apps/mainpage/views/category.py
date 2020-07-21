from django.views.generic import ListView

from .. import sidebar
from .dataset import DatasetForm

class CategoryView(ListView):
    """
        List Datasets by type
    """
    template_name = 'mainpage/category-index.html'
    context_object_name = "datasets"

    form = None

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        if not self.form:
            self.form = DatasetForm
        context.update({
            'form': self.form
        })
        return context

    def get_queryset(self):
        return sidebar.get_ds_subjects_list(None)
