from django import forms
from optimer.models import optimer

def get_fleet_list():
    fleets = optimer.objects.all()
    fleetlist = [("None", "None")]
    for fleet in fleets:
        fleetlist.append((fleet.operation_name, fleet.operation_name))
    fleetlist.sort()
    return fleetlist


class PaplinkForm(forms.Form):
    papname = forms.CharField(label='Name of pap', required=True)
    duration = forms.IntegerField(label="Duration of pap", required=True, initial=30)
    vip_count = forms.CharField(widget=forms.HiddenInput())
    fleet = forms.ChoiceField(label="Fleet", choices=get_fleet_list())

    def __init__(self, *args, **kwargs):
        n_vips = kwargs.pop('extra', 0)

        super(PaplinkForm, self).__init__(*args, **kwargs)
        self.fields['vip_count'].initial = n_vips
        for index in range(int(n_vips)):
            self.fields['vip_{index}'.format(index=index)] = forms.CharField(required=False)