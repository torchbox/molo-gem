from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from django.views.generic.base import View

from wagtail.wagtailadmin import messages
from wagtail.wagtailadmin.utils import permission_required
from wagtail.wagtailcore import hooks
from wagtail.wagtailusers.forms import GroupPagePermissionFormSet
from wagtail.wagtailusers.views.groups import get_permission_panel_classes

from .forms import CSVGroupCreationForm


@permission_required('auth.add_group')
def create(request):
    group = Group()
    if request.method == 'POST':
        form = CSVGroupCreationForm(request.POST, request.FILES, instance=group)
        permission_panels = [
            cls(request.POST, instance=group)
            for cls in get_permission_panel_classes()
        ]

        if form.is_valid() and all(panel.is_valid() for panel in permission_panels):
            form.save()

            for panel in permission_panels:
                panel.save()

            messages.success(request, _("Group '{0}' created.").format(group), buttons=[
                messages.button(reverse('wagtailusers_groups:edit', args=(group.id,)), _('Edit'))
            ])
            return redirect('wagtailusers_groups:index')
        else:
            messages.error(request, _("The group could not be created due to errors."))
    else:
        form = CSVGroupCreationForm(instance=group)
        permission_panels = [
            cls(instance=group)
            for cls in get_permission_panel_classes()
        ]

    return render(request, 'csv_group_creation/create.html', {
        'form': form,
        'permission_panels': permission_panels,
    })
