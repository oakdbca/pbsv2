from django.db import models
from django.views.generic import base


class BaseView(base.ContextMixin, base.TemplateResponseMixin, base.View):
    """Simple base view to render detail views in the project."""

    context_object_name = None
    template_name = "govapp/index.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context["object"] = self.object
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
        context.update(kwargs)
        return super().get_context_data(**context)

    def get_context_object_name(self, obj):
        if self.context_object_name:
            return self.context_object_name
        elif isinstance(obj, models.Model):
            return obj._meta.model_name
        else:
            return None

    def get_template_names(self) -> list[str]:
        template_names = super().get_template_names()
        return template_names

    def get_object(self, queryset=None):
        pk = self.kwargs.get("pk", None)
        if pk:
            return self.model.objects.get(pk=pk)
        return None
