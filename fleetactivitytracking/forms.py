from django import forms
from optimer.models import optimer

def get_fleet_list():
    fleets = optimer.objects.all()
    fleetlist = [("None", "None")]
    for fleet in fleets:
        fleetlist.append((fleet.operation_name, fleet.operation_name))
    fleetlist.sort()
    return fleetlist


class FatlinkForm(forms.Form):
    fatname = forms.CharField(label='Name of fat-link', required=True)
    duration = forms.IntegerField(label="Duration of fat-link", required=True, initial=30, min_value=1, max_value=2147483647)
    fleet = forms.ModelChoiceField(label="Operation", queryset=optimer.objects.all().order_by('operation_name'), empty_label="No operation", required=False)
