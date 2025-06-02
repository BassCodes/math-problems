from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

from .models import DraftRef
from .forms import ConfirmForm


def draft_create_view_factory(model, fields):
    new_classname = f"{model.__name__}CreateView"
    attributes = {}
    attributes["model"] = model
    attributes["fields"] = fields
    # todo
    attributes["success_url"] = reverse_lazy("home")
    attributes["form_valid"] = None
    attributes["template_name"] = "editor/generic_draft_create.html"
    new_class = type(new_classname, (CreateView,), attributes)

    def form_valid(self, form):
        new_ref = DraftRef.create_new(self.request.user)
        new_ref.save()
        form.instance.draft_ref = new_ref
        return super(new_class, self).form_valid(form)

    new_class.form_valid = form_valid

    return new_class


# TODO Auth
def draft_delete_view_factory(model):
    new_classname = f"{model.__name__}Delete"
    attributes = {}

    def get_success_url(self, **kwargs):
        return reverse_lazy("user_drafts", kwargs={"pk": self.request.user.pk})

    attributes["model"] = model
    attributes["template_name"] = "editor/generic_draft_confirm_delete.html"
    attributes["get_success_url"] = get_success_url
    return type(new_classname, (LoginRequiredMixin, DeleteView), attributes)


# TODO Auth
def draft_detail_view_factory(model, template, object_name):
    new_classname = f"{model.__name__}View"
    attributes = {}
    attributes["model"] = model
    attributes["template_name"] = template
    attributes["get_context_data"] = None
    new_class = type(new_classname, (DetailView,), attributes)

    def get_context_data(self, **kwargs):
        context = super(new_class, self).get_context_data(**kwargs)
        context[object_name] = context["object"]
        return context

    new_class.get_context_data = get_context_data
    return new_class


def draft_force_publish_factory(model):
    new_classname = f"{model.__name__}ForcePublishView"
    attributes = {}
    attributes["model"] = model
    attributes["form_class"] = ConfirmForm
    attributes["template_name"] = "editor/generic_confirm_force_publish.html"

    def form_valid(self, form):
        if self.object.draft_ref.draft_state == DraftRef.DraftState.DRAFT:
            self.object.send_to_review()
        published = self.object.publish()
        return HttpResponseRedirect(published.get_absolute_url())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    attributes["form_valid"] = form_valid
    attributes["post"] = post

    new_class = type(new_classname, (FormMixin, DetailView), attributes)

    return new_class


def draft_edit_view_factory(model, fields, template_name="editor/generic_draft_edit.html"):
    new_classname = f"{model.__name__}UpdateView"
    attributes = {}
    attributes["model"] = model
    attributes["fields"] = fields
    attributes["template_name"] = template_name
    attributes["success_url"] = reverse_lazy("home")

    new_class = type(new_classname, (UpdateView,), attributes)
    return new_class


def fork_factory(model, draft_model):
    new_classname = f"{model.__name__}ForkView"
    attributes = {}
    attributes["model"] = model
    attributes["form_class"] = ConfirmForm
    attributes["template_name"] = "editor/generic_confirm_fork.html"

    def form_valid(self, form):
        draft = draft_model.create_new(self.request.user, forked_from=self.object)
        return HttpResponseRedirect(draft.get_absolute_url())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    attributes["form_valid"] = form_valid
    attributes["post"] = post

    new_class = type(new_classname, (FormMixin, DetailView), attributes)

    def get_context_data(self, **kwargs):
        context = super(new_class, self).get_context_data(**kwargs)

        existing_ref = DraftRef.objects.by_owner(self.request.user).by_forked(context["object"]).first()

        context["existing"] = draft_model.objects.filter(draft_ref=existing_ref).first()

        return context

    new_class.get_context_data = get_context_data

    return new_class
