# -*- coding: utf-8 -*-
#
# webb.org
# Copyright 2010-2015 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>

from collections import OrderedDict

from django.http import JsonResponse
from django.views.generic.base import TemplateView

from djangoplicity.announcements.models import Announcement
from djangoplicity.media.models import Image, Video, PictureOfTheWeek
from djangoplicity.media.options import ImageOptions, VideoOptions, PictureOfTheWeekOptions, PictureOfTheMonthOptions
from djangoplicity.newsletters.models import Newsletter, NewsletterType
from djangoplicity.releases.models import Release
from djangoplicity.metadata.models import CategoryType

from webb.frontpage.models import Highlight


class FrontpageView(TemplateView):

    template_name = 'frontpage.html'

    def get_context_data(self, **kwargs):
        context = super(FrontpageView, self).get_context_data(**kwargs)
        context['announcements'] = Announcement.get_latest_announcement(4, only_featured=True)
        context['highlights'] = Highlight.objects.filter(published=True)
        # TODO: Check why this is not working
        context['spacesparks'] = VideoOptions.Queries.category.queryset(Video, VideoOptions, self.request, stringparam='spacesparks')[0].order_by('-release_date',)[:4]
        context['potws'] = PictureOfTheWeekOptions.Queries.default.queryset(PictureOfTheWeek, PictureOfTheWeekOptions, self.request, stringparam='potws')[0].order_by('-release_date',)[:1]
        context['potms'] = PictureOfTheMonthOptions.Queries.default.queryset(PictureOfTheWeek, PictureOfTheMonthOptions, self.request, stringparam='potms')[0].order_by('-release_date',)[:4]
        context['releases'] = Release.get_latest_release(4)

        return context


def d2d():
    '''
    Generic "Data provide" D2D feed
    '''
    return JsonResponse(OrderedDict([
        ('Creator', 'ESA/Hubble'),
        ('URL', 'https://www.webb.org'),
        ('Contact', OrderedDict([
            ('Name', 'Lars Lindberg Christensen'),
            ('Email', 'lars@eso.org'),
            ('Telephone', '+498932006761'),
            ('Address', 'Karl-Schwarzschild-Strasse 2'),
            ('City', 'Garching bei München'),
            ('StateProvince', 'Bavaria'),
            ('PostalCode', '85748'),
            ('Country', 'Germany'),
        ])),
        ('Logo', 'https://www.webb.org/static/archives/logos/medium/esa_screen_blue.jpg'),
        ('Feeds', [
            {
                'Name': 'ESA/Hubble Images',
                'Description': 'ESA/Hubble Images',
                'URL': 'https://www.webb.org/images/d2d/',
                'Type': 'Images',
            },
            {
                'Name': 'ESA/Hubble Videos',
                'Description': 'ESA/Hubble Videos',
                'URL': 'https://www.webb.org/videos/d2d/',
                'Type': 'Videos',
            },
        ]
        ),
    ]))
