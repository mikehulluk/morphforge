#-------------------------------------------------------------------------------
# Copyright (c) 2012 Michael Hull.
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
# 
#  - Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#  - Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#-------------------------------------------------------------------------------
from django.conf.urls.defaults import *

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()
from django.conf import settings


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


p = (
    # Example:
    # (r'^simmgr/', include('simmgr.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
    (r'^simulationfileruns/(\d+)', 'sm1.views.simulationfilerun_details'),
    (r'^simulationfileruns/(\d+)', 'sm1.views.simulationfile_details'),
    (r'^viewpotentialsimulationfiles$', 'sm1.views.viewpotentialsimulationfiles'),
    (r'^viewsimulationqueue$', 'sm1.views.viewsimulationqueue'),
    (r'^do/update_potential_simulation_files', 'sm1.views.doupdatepotentialsimulationfiles'),
    (r'^do/potential_to_actual_simulation', 'sm1.views.dopotentialtoactualsimulationfiles'),
    (r'^do/queuesimulations', 'sm1.views.doqueuesimulations'),
    (r'^do/removesimulationsfromqueue', 'sm1.views.doremovesimulationsfromqueue'),
    (r'^do/editsimulationfile/(\d+)', 'sm1.views.doeditsimulationfile'),

    (r'^simulationfiles/(\d+)$', 'sm1.views.simulationfile_details'),
    (r'^do/addpotentialsimulationlocation', 'sm1.views.doaddpotentialsimulationlocation'),

    (r'^$', 'sm1.views.index'),

    (r'^mh/add_default_locations', 'sm1.views.mh_adddefault_locations'),

    (r'^viewsimulationfailures$', 'sm1.views.view_simulation_failures'),

    (r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
)


p = p + (
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/michael/hw/morphforge/src/mhlibs/simulation_manager/simmgr/static/'}),
    (r'^site_media/javascript/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/michael/hw/morphforge/src/mhlibs/simulation_manager/simmgr/static/javascript/'}),
    )



urlpatterns = patterns('', *p)
