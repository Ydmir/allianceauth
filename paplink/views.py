from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.template import RequestContext
from django.http import HttpResponseBadRequest
from django.core.exceptions import ValidationError
from django.utils import timezone

from eveonline.models import EveCharacter
from eveonline.managers import EveManager
from util import check_if_user_has_permission
from forms import PaplinkForm
from models import Paplink
from models import VipPap
from models import Pap

from slugify import slugify

import datetime


import logging

logger = logging.getLogger(__name__)

@login_required
def paplink_view(request):
    # Will show the last 5 or so paplinks clicked by user.
    # If the user has the right privileges the site will also show the latest paplinks with the options to add VIPs and
    # manually add players.
    #TODO: ADd functionality to step further back in the pap-history. See clicked paplinks by month for example.
    user = request.user
    logger.debug("paplink_view called by user %s" % request.user)

    latest_paps = Pap.objects.filter(user=user).order_by('-id')[:5]
    if check_if_user_has_permission(user, 'paplink'):
        latest_links = Paplink.objects.all().order_by('-id')[:5]
        context = {'user':user, 'paps': latest_paps, 'paplinks': latest_links}

    else:
        context = {'user':user, 'paps': latest_paps}


    return render_to_response('registered/paplinkview.html', context, context_instance=RequestContext(request))

def paplink_statistics_view(request):
    #TODO: Some fancy statistics. Paps per corp. Paps/active member. Paps/Character. Other metrics. Run in background tasks.
    return


@login_required
def click_paplink_view(request, papname):
    # Take IG-header data and register the pap if not existing already.
    # use obj, created = Pap.objects.get_or_create()
    # onload="CCPEVE.requestTrust('http://www.mywebsite.com')"

    # TODO: Probably a check for if we are using the IGB at all should be performed..
    if 'HTTP_EVE_TRUSTED' in request.META and request.META['HTTP_EVE_TRUSTED'] == "Yes":
        # Retrieve the latest pap using the link.
        try:
            paplink = Paplink.objects.filter(name=papname).latest(field_name="papdatetime")
            valid = True
            print "---------------"
            print timezone.now()
            print paplink.papdatetime
            print datetime.timedelta(seconds=(paplink.duration*60))
            print (timezone.now() - paplink.papdatetime)

            if (timezone.now() - paplink.papdatetime) < datetime.timedelta(seconds=(paplink.duration*60)):
                active = True

                character = EveManager.get_character_by_id(request.META['HTTP_EVE_CHARID'])

                if character:
                    pap = Pap()
                    pap.system = request.META['HTTP_EVE_SOLARSYSTEMNAME']
                    pap.station = request.META['HTTP_EVE_STATIONNAME']
                    pap.shiptype = request.META['HTTP_EVE_SHIPTYPENAME']
                    pap.paplink = paplink
                    pap.character = character
                    pap.user = character.user
                    try:
                        pap.full_clean()
                        pap.save()
                        context = {'trusted': True, 'registered': True}
                    except ValidationError as e:
                        messages = []
                        for errorname, message in e.message_dict.items():
                            messages.append(message[0].decode())
                        context = {'trusted': True, 'errormessages': messages}
                else:
                    context = {'character_id': request.META['HTTP_EVE_CHARID'], 'character_name': request.META['HTTP_EVE_CHARNAME']}
                    return render_to_response('public/characternotexisting.html', context, context_instance=RequestContext(request))
            else:
                context = {'trusted': True, 'expired': True}
        except ObjectDoesNotExist:
            context = {'trusted': True}
    else:
        context = {'trusted': False, 'papname': papname}
    return render_to_response('public/clickpaplinkview.html', context, context_instance=RequestContext(request))


@login_required
@permission_required('auth.paplink')
def create_paplink_view(request):
    logger.debug("create_paplink_view called by user %s" % request.user)
    if request.method == 'POST':
        logger.debug("Post request to create_paplink_view by user %s" % request.user)
        form = PaplinkForm(request.POST, extra=request.POST.get('vip_count'))
        if 'add_extra_vip' in request.POST:
            if form.is_valid():
                form.vip_count = int(form.cleaned_data["vip_count"])+1
            else:
                form = PaplinkForm()
        elif 'submit_pap' in request.POST:
            logger.debug("Submitting paplink by user %s" % request.user)
            if form.is_valid():
                paplink = Paplink()
                paplink.name = slugify(form.cleaned_data["papname"])
                paplink.fleet = form.cleaned_data["fleet"]
                paplink.duration = form.cleaned_data["duration"]
                paplink.creator = request.user
                try:
                    paplink.full_clean()
                    paplink.save()
                except ValidationError as e:
                    form = PaplinkForm()
                    messages = []
                    for errorname, message in e.message_dict.items():
                        messages.append(message[0].decode())
                    context = {'form': form, 'errormessages': messages}
                    return render_to_response('registered/paplinkformatter.html', context, context_instance=RequestContext(request))

                for vipnr in range(int(form.cleaned_data["vip_count"])):
                    vippap = VipPap()
                    vippap.character = form.cleaned_data["vip_%s" % vipnr]
                    vippap.paplink = paplink
                    vippap.save()
            else:
                form = PaplinkForm()
                context = {'form': form, 'badrequest': True}
                return render_to_response('registered/paplinkformatter.html', context, context_instance=RequestContext(request))
            return HttpResponseRedirect('/pap/')

    else:
        form = PaplinkForm()
        logger.debug("Returning empty form to user %s" % request.user)

    context = {'form': form}

    return render_to_response('registered/paplinkformatter.html', context, context_instance=RequestContext(request))


@login_required
@permission_required('auth.paplink')
def modify_paplink_view(request, datestr=None, papname=""):
    logger.debug("modify_paplink_view called by user %s" % request.user)
    if not papname:
        return HttpResponseRedirect('/pap/')

    date = datetime.datetime.strptime(datestr, "%Y-%m-%d").date()

    paplink = Paplink.objects.filter(name=papname).filter(papdate=date)

    context = {}

    return render_to_response('registered/paplinkformatter.html', context, context_instance=RequestContext(request))