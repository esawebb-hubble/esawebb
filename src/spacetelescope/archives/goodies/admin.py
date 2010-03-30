# Djangoplicity
# Copyright 2007-2008 ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#
from django.conf import settings
from django.contrib import admin
from djangoplicity.contrib.admin import DjangoplicityModelAdmin
from spacetelescope.archives.goodies.models import *
from djangoplicity.archives.contrib.admin import ArchiveAdmin, RenameAdmin, view_link
from django.forms import ModelForm
from django.core.urlresolvers import NoReverseMatch, reverse
from django.utils.safestring import mark_safe



class CalendarAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'year', 'month','priority','last_modified', 'published',view_link('calendars') )
	list_filter = ( 'year', 'month', 'published', 'last_modified',  )
	list_editable = ( 'published', )
	search_fields = ( 'id', 'old_ids', 'title', 'description', 'credit' )
	date_hierarchy = 'last_modified'
	fieldsets = (
					( None, {'fields': ( 'id', ) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'year', 'month', 'description', 'credit', ), } ),
					( 'Compatibility', {'fields': ('old_ids', ), }),
				)
	ordering = ('id', )
	richtext_fields = ('description',)
	links = ()
	

def artist (obj):
	return 	obj.artist.name.encode('ascii')

#TODO: artist unicode problems on ADMIN!?!?
class OnlineArtAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'title', 'published','priority','last_modified', view_link('art') )
	list_filter = ( 'title', 'published', 'last_modified', )
	list_editable = ( 'title', 'published', )
	search_fields = ( 'id', 'old_ids', 'title', 'description', 'artist', 'credit' )
	date_hierarchy = 'last_modified'
	fieldsets = (
					( None, {'fields': ( 'id', ) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'title', 'description', 'credit', 'artist'), } ),
					( 'Compatibility', {'fields': ('old_ids', ), }),
				)
	ordering = ('id', )
	raw_id_fields = ('artist', )
	richtext_fields = ('description',)

	links = ()
	
class OnlineArtAuthorAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'name', 'city', 'country', 'email', )
	list_filter = ( 'city', 'country',)
	search_fields = ( 'name', 'city', 'country', 'email',)
	fieldsets = (
					( None,  {'fields': ( 'name', 'description', 'city', 'country', 'email', ), } ),
					
				)
	ordering = ('name', )
	richtext_fields = ('description',)
	links = ()

#TODO printlayouts remain?
#class PrintLayoutAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
#	list_display = ( 'id', 'title', 'published','priority','last_modified', view_link('printlayouts') )
#	list_filter = ( 'title', 'published', 'last_modified', )
#	list_editable = ( 'title', 'published', )
#	search_fields = ( 'id', 'old_ids', 'title', 'description', 'credit' )
#	date_hierarchy = 'last_modified'
#	fieldsets = (
#					( None, {'fields': ( 'id', ) } ),
#					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
#					( 'Archive', {'fields': ( 'title', 'description', 'credit', ), } ),
#					( 'Compatibility', {'fields': ('old_ids', ), }),
#				)
#	ordering = ('id', )
#	richtext_fields = ('description',)
#
#	links = ()


class SlideShowAdmin( DjangoplicityModelAdmin, RenameAdmin, ArchiveAdmin ):
	list_display = ( 'id', 'title', 'published','priority','last_modified', 'resolution','x_size','y_size', view_link('slideshows') )
	list_filter = ( 'title', 'published', 'last_modified', 'resolution','x_size','y_size')
	list_editable = ( 'title', 'published', 'resolution','x_size','y_size' )
	search_fields = ( 'id', 'old_ids', 'title', 'description', 'credit' )
	date_hierarchy = 'last_modified'
	fieldsets = (
					( None, {'fields': ( 'id', ) } ),
					( 'Publishing', {'fields': ( 'published', 'priority', ), } ),
					( 'Archive', {'fields': ( 'title', 'description', 'credit', ), } ),
					( 'Screen', {'fields': ( 'resolution', 'x_size', 'y_size'), } ),
					( 'Compatibility', {'fields': ('old_ids', ), }),
				)
	ordering = ('id', )
	richtext_fields = ('description',)

	links = ()


def register_with_admin( admin_site ):
	admin_site.register( Calendar, CalendarAdmin )
	admin_site.register( OnlineArt, OnlineArtAdmin )
	admin_site.register( OnlineArtAuthor, OnlineArtAuthorAdmin )
	#admin_site.register( PrintLayout, PrintLayoutAdmin )
	admin_site.register( SlideShow, SlideShowAdmin )
	
# Register with default admin site	
register_with_admin( admin.site )