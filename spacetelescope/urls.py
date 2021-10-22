# -*- coding: utf-8 -*-
#
# spacetelescope.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

import django.views
import django.views.defaults

from django.conf import settings
from django.conf.urls import include, url
from django.views.decorators.cache import cache_page
from django.views.generic.base import RedirectView

import djangoplicity.views
from djangoplicity.announcements.models import Announcement, WebUpdate
from djangoplicity.announcements.options import AnnouncementOptions, WebUpdateOptions
from djangoplicity.media.models import Image, Video, PictureOfTheWeek, ImageComparison
from djangoplicity.media.options import ImageOptions, VideoOptions, PictureOfTheWeekOptions, ImageComparisonOptions
from djangoplicity.menus.views import sitemap
from djangoplicity.newsletters.models import Newsletter
from djangoplicity.newsletters.options import NewsletterOptions
from djangoplicity.pages.views import view_page
from djangoplicity.products.models import *
from djangoplicity.products.options import *
from djangoplicity.releases.models import Release
from djangoplicity.releases.options import ReleaseOptions
from djangoplicity.science.models import ScienceAnnouncement
from djangoplicity.science.options import ScienceAnnouncementOptions

from spacetelescope.admin import admin_site, adminlogs_site, adminshop_site
from spacetelescope.frontpage.views import FrontpageView, d2d

urlpatterns = []

if not settings.DEBUG:
    urlpatterns += [
        url( r'^%s(?P<path>.*)' % settings.MEDIA_URL[1:], djangoplicity.archives.contrib.security.views.serve_static_file),
    ]

if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

urlpatterns += [

    # Djangoplicity Adminstration
    url( r'^admin/cache/', include( 'djangoplicity.cache.urls', namespace="admincache_site", app_name="cache" )),
    url( r'^admin/history/', include( 'djangoplicity.adminhistory.urls', namespace="adminhistory_site", app_name="history" )),
    url( r'^admin/doc/', include( 'django.contrib.admindocs.urls' )),
    url( r'^admin/shop/', include( 'djangoplicity.archives.contrib.satchmo.urls_admin' ) ),
    url( r'^admin/shop/', include(adminshop_site.urls), { 'extra_context': { 'ADMINSHOP_SITE': True } } ),
    url( r'^admin/system/', include(adminlogs_site.urls), { 'extra_context': { 'ADMINLOGS_SITE': True }  } ),
    url( r'^admin/', include(admin_site.urls), { 'extra_context': { 'ADMIN_SITE': True }  } ),
    url( r'^admin/import/', include('djangoplicity.archives.importer.urls') ),
    url( r'^admin/', include('djangoplicity.metadata.wtmlimport.urls'), { 'extra_context': { 'ADMIN_SITE': True }  } ),
    url( r'^public/djangoplicity/admin/reportsdetails/', include( 'djangoplicity.reports.urls' ) ),
    url(r'^tinymce/', include('tinymce.urls')),

    # Djangoplicity pages API
    url( r'^public/djangoplicity/admin/pages/', include('djangoplicity.pages.urls') ),

    # Server alive check (used for load balancers - called every 5 secs )
    url( r'^alive-check.dat$', djangoplicity.views.alive_check ),

    # Media Archive
    url( r'^images/potw/', include('djangoplicity.media.urls_potw'), { 'model': PictureOfTheWeek, 'options': PictureOfTheWeekOptions } ),
    url( r'^images/comparisons/', include('djangoplicity.media.urls_imagecomparisons'), { 'model': ImageComparison, 'options': ImageComparisonOptions } ),
    url( r'^images/', include('djangoplicity.media.urls_images'), { 'model': Image, 'options': ImageOptions } ),
    #( r'^news/feed/(?P<url>.*)/?$', 'django.contrib.syndication.views.feed', { 'feed_dict': ReleaseOptions.get_feeds() } ),
    url( r'^news/', include('djangoplicity.releases.urls'), { 'model': Release, 'options': ReleaseOptions } ),
    url( r'^videos/uservideos/', include('djangoplicity.products.urls.uservideos'), { 'model': UserVideo, 'options': UserVideoOptions } ),
    url( r'^videos/', include('djangoplicity.media.urls_videos'), { 'model': Video, 'options': VideoOptions } ),

    # Other archives
    url( r'^announcements/webupdates/', include('djangoplicity.announcements.urls_webupdates'), { 'model': WebUpdate, 'options': WebUpdateOptions } ),
    url( r'^announcements/', include('djangoplicity.announcements.urls'), { 'model': Announcement, 'options': AnnouncementOptions } ),

    ### ENTIRE BLOCK REFERENCING djangoplicity.products
    url( r'^about/further_information/books/', include('djangoplicity.products.urls.books'), { 'model': Book, 'options': BookOptions } ),
    url( r'^about/further_information/brochures/', include('djangoplicity.products.urls.brochures'), { 'model': Brochure, 'options': BrochureOptions } ),
    url( r'^about/further_information/flyers/', include('djangoplicity.products.urls.flyers'), { 'model': Flyer, 'options': FlyerOptions } ),
    url( r'^about/further_information/handouts/', include('djangoplicity.products.urls.handouts'), { 'model': Handout, 'options': HandoutOptions } ),
    url( r'^about/further_information/maps/', include('djangoplicity.products.urls.maps'), { 'model': Map, 'options': MapOptions } ),
    url( r'^about/further_information/messengers/', include('djangoplicity.products.urls.messengers'), { 'model': Messenger, 'options': MessengerOptions } ),
    url( r'^about/further_information/schools/', include('djangoplicity.products.urls.schools'), { 'model': ScienceInSchool, 'options': ScienceInSchoolOptions } ),
    url( r'^about/further_information/capjournals/', include('djangoplicity.products.urls.capjournals'), { 'model': CapJournal, 'options': CapJournalOptions } ),
    url( r'^about/further_information/stecfnewsletters/', include('djangoplicity.products.urls.stecfnewsletters'), { 'model': STECFNewsletter, 'options': STECFNewsletterOptions } ),
    url( r'^about/further_information/bulletins/', include('djangoplicity.products.urls.bulletins'), { 'model': Bulletin, 'options': BulletinOptions } ),
    url( r'^about/further_information/techdocs/', include('djangoplicity.products.urls.techdocs'), { 'model': TechnicalDocument, 'options': TechnicalDocumentOptions } ),
    url( r'^products/calendars/', include('djangoplicity.products.urls.calendars'), { 'model': Calendar, 'options': CalendarOptions } ),
    url( r'^products/applications/', include('djangoplicity.products.urls.applications'), { 'model': Application, 'options': ApplicationOptions } ),
    url( r'^products/art/', include('djangoplicity.products.urls.art'), { 'model': OnlineArt, 'options': OnlineArtOptions } ),
    url( r'^products/artists/', include('djangoplicity.products.urls.artists'), { 'model': OnlineArtAuthor, 'options': OnlineArtAuthorOptions } ),
    url( r'^products/logos/', include('djangoplicity.products.urls.logos'), { 'model': Logo, 'options': LogoOptions } ),
    url( r'^products/exhibitions/', include('djangoplicity.products.urls.exhibitions'), { 'model': Exhibition, 'options': ExhibitionOptions } ),
    url( r'^products/stickers/', include('djangoplicity.products.urls.stickers'), { 'model': Sticker, 'options': StickerOptions } ),
    url( r'^products/postcards/', include('djangoplicity.products.urls.postcards'), { 'model': PostCard, 'options': PostCardOptions } ),
    url( r'^products/print_posters/', include('djangoplicity.products.urls.print_posters'), { 'model': PrintedPoster, 'options': PrintedPosterOptions } ),
    url( r'^products/conf_posters/', include('djangoplicity.products.urls.conf_posters'), { 'model': ConferencePoster, 'options': ConferencePosterOptions } ),
    url( r'^products/elec_posters/', include('djangoplicity.products.urls.elec_posters'), { 'model': ElectronicPoster, 'options': ElectronicPosterOptions } ),
    url( r'^products/apparel/', include('djangoplicity.products.urls.apparels'), { 'model': Apparel, 'options': ApparelOptions } ),
    url( r'^products/merchandise/', include('djangoplicity.products.urls.merchandise'), { 'model': Merchandise, 'options': MerchandiseOptions } ),
    url( r'^products/media/', include('djangoplicity.products.urls.media'), { 'model': Media, 'options': MediaOptions } ),
    url( r'^products/imaxfilms/', include('djangoplicity.products.urls.imaxfilms'), { 'model': IMAXFilm, 'options': IMAXFilmOptions } ),
    url( r'^products/presentations/', include('djangoplicity.products.urls.presentations'), { 'model': Presentation, 'options': PresentationOptions } ),
    url( r'^products/models3d/', include('djangoplicity.products.urls.models3d'), { 'model': Model3d, 'options': Model3dOptions, 'translate': False } ),
    url( r'^kidsandteachers/education/', include('djangoplicity.products.urls.education'), { 'model': EducationalMaterial, 'options': EducationalMaterialOptions } ),
    url( r'^kidsandteachers/drawings/', include('djangoplicity.products.urls.drawings'), { 'model': KidsDrawing, 'options': KidsDrawingOptions } ),
    url( r'^press/kits/', include('djangoplicity.products.urls.presskits'), { 'model': PressKit, 'options': PressKitOptions } ),
    
    url( r'^forscientists/announcements/', include('djangoplicity.science.urls'), { 'model': ScienceAnnouncement, 'options': ScienceAnnouncementOptions } ),

    url( r'^projects/fits_liberator/fitsimages/', include('djangoplicity.products.urls.fitsimages'), { 'model': FITSImage, 'options': FITSImageOptions } ),

    url( r'^rss/feed.xml$', RedirectView.as_view(url='http://feeds.feedburner.com/hubble_news/') ),
    url( r'^rss/vodcast.xml$', RedirectView.as_view(url='http://feeds.feedburner.com/hubblecast_sd/') ),
    url( r'^rss/vodcasthd.xml$', RedirectView.as_view(url='http://feeds.feedburner.com/hubblecast/') ),
    url( r'^rss/vodcastfullhd.xml$', RedirectView.as_view(url='http://feeds.feedburner.com/hubblecast_fullhd/') ),
    url( r'^rss/hubblecasthd_amp.xml$', RedirectView.as_view(url='http://feeds.feedburner.com/hubblecast/') ),

    # User authentication
    url( r'^login/$', django.contrib.auth.views.login, { 'template_name': 'login.html' } ),
    url( r'^logout/$', django.contrib.auth.views.logout, { 'template_name': 'logout.html' } ),
    url( r'^password_reset/$', django.contrib.auth.views.password_reset, { 'email_template_name': 'registration/password_reset_email.txt' }, name='password_reset' ),
    url( r'^password_reset/done/$', django.contrib.auth.views.password_reset_done, name='password_reset_done' ),
    url( r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', django.contrib.auth.views.password_reset_confirm, name='django.contrib.auth.views.password_reset_confirm' ),
    url( r'^reset/done/$', django.contrib.auth.views.password_reset_complete, name='password_reset_complete' ),

    # Shop
    url( r'^shop/terms/', RedirectView.as_view(url='/shop/terms_conditions/'), name='shop_terms' ),
    url( r'^shop/ccv/', RedirectView.as_view(url='/shop/cvc_info/'), name='shop_ccv' ),
    url( r'^shop/bulkorders/', RedirectView.as_view(url='/shop/bulk_orders/'), name='shop_bulkorders' ),
    url( r'^shop/freeorder/', include( 'djangoplicity.archives.contrib.satchmo.freeorder.urls' ) ),
    url( r'^shop/', include( 'djangoplicity.archives.contrib.satchmo.urls' ) ),
    url( r'^newsletters/', include( 'djangoplicity.mailinglists.urls', namespace='djangoplicity_mailinglists', app_name='djangoplicity_mailinglists' ) ),
    url( r'^newsletters/', include( 'djangoplicity.newsletters.urls'), { 'model': Newsletter, 'options': NewsletterOptions, } ),
    #( r'^public/djangoplicity/events/', include('djangoplicity.events.urls'), { 'model': Event, 'options': EventOptions } ),
    url( r'^facebook/', include('djangoplicity.iframe.urls')  ),

    # Main view
    url( r'^$', cache_page(60 * 5)(FrontpageView.as_view()) ),

    # Sitemap
    url(r'^sitemap/$', sitemap),

    url( r'^d2d/$', d2d ),

    # Static pages
    url(r'^(?P<url>.*/)$', view_page)
]

#handler404 = 'spacetelescope.views.page_not_found'

# Static files/media serving during development
if settings.SERVE_STATIC_MEDIA:
    urlpatterns += [
        url( r'^' + settings.DJANGOPLICITY_MEDIA_URL[1:] + r'(?P<path>.*)$', django.views.static.serve, {'document_root': settings.DJANGOPLICITY_MEDIA_ROOT, 'show_indexes': True } ),
        url( r'^' + settings.MEDIA_URL[1:] + r'(?P<path>.*)$', django.views.static.serve, {'document_root': settings.MEDIA_ROOT, 'show_indexes': True } ),
    ]
