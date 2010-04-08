from django.conf import settings
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import Site
from djangoplicity.logger import define_logger
from djangoplicity.media.models import Image
from djangoplicity.migration import run_migration
from djangoplicity.migration.apps.archives import ArchiveInitializationTask, \
	ArchiveMigrationTask, DataMapping
from djangoplicity.migration.apps.pages import PageInitializationTask, \
	PageMigrationTask, HTMLPageDocument
from djangoplicity.pages.models import Section
from djangoplicity.releases.models import Release
from spacetelescope.archives.educational.models import *
from spacetelescope.archives.goodies.models import *
from spacetelescope.archives.products.models import *
from spacetelescope.migration.archives import *
from spacetelescope.migration.pages import SpacetelescopePageDocument, \
	SpacetelescopePageLinksCleanupTask, SpacetelescopePageFilesCopyTask
import logging
import re

#
# Define logger to use
#
logger = define_logger( "migration_logger", level=logging.DEBUG, file_logging=False )
	
#
# Define configuration options
#
conf = {
	'media_root' : '/hubbleroot/',
	'pages' : {
				'root' : '/Volumes/webdocs/spacetelescope/docs/', 
				'site' : Site.objects.get(id=settings.SITE_ID), 
				'section' : Section.objects.get_or_create( name='Default', append_title='spacetelescope.org', template='pages/page_onecolumn.html' )[0],
				'sections' : { 
								'home' : Section.objects.get_or_create( name='Home', append_title='spacetelescope.org', template='pages/page_onecolumn.html' )[0],
								'news' : Section.objects.get_or_create( name='News', append_title='News | spacetelescope.org', template='pages/page_onecolumn.html' )[0],
								'images' : Section.objects.get_or_create( name='Images', append_title='Images | spacetelescope.org', template='pages/page_onecolumn.html' )[0],
								'videos' : Section.objects.get_or_create( name='Videos', append_title='Videos | spacetelescope.org', template='pages/page_onecolumn.html' )[0],
								'shop' : Section.objects.get_or_create( name='Shop', append_title='Hubble Shop | spacetelescope.org', template='pages/page_onecolumn.html' )[0],
								'extras' : Section.objects.get_or_create( name='Hubble Extras', append_title='Hubble Extras | spacetelescope.org', template='pages/page_onecolumn.html' )[0],
								'about' : Section.objects.get_or_create( name='About Hubble', append_title='About Hubble | spacetelescope.org', template='pages/page_onecolumn.html' )[0],
								'kids' : Section.objects.get_or_create( name='Kids & Teachers', append_title='Kids & Teachers | spacetelescope.org', template='pages/page_onecolumn.html' )[0],
								'press' : Section.objects.get_or_create( name='Press', append_title='Press | spacetelescope.org', template='pages/page_onecolumn.html' )[0],
								'projects' : Section.objects.get_or_create( name='Projects', append_title='Projects | spacetelescope.org', template='pages/page_onecolumn.html' )[0],
							 },
				'section_mapping' : {
								'news' : 'news',
								'home' : 'home',
								'images' : 'images',
								'videos' : 'videos',
								'goodies' : 'extras',
								'hubble shop' : 'shop',
								'science' : 'about',
								'about hubble' : 'about',
								'kids &amp; teachers' : 'kids',
								'press' : 'press',
								'projects' : 'projects',
								'jobs' : 'default',
							},
			  },
	'logger' : 'migration_logger', 
}


redirectpatterns = [
	( re.compile( "^(/news|/images|/videos|/updates|/about/further_information/brochures|/about/further_information/newsletters|/about/further_information/presskits)/html/([a-z0-9_-]+)\.html$" ), "\g<1>/\g<2>/" ),
	( re.compile( "^/index\.html$" ), "/" ),
	( re.compile( "^/bin/images\.pl\?string=([a-z0-9-_]+)$" ), "/images/\g<1>/" ),
	( re.compile( "^/images/(news|screen|thumbs|medium|web)/([a-z0-9-_]+)\.(jpg|tif)$" ), "/static/archives/images/\g<1>/\g<2>.\g<3>" ),
	( re.compile( "^/about_us/logos/(news|screen|thumbs|medium|web)/([a-z0-9-_]+)\.(jpg|tif)$" ), "/static/archives/images/\g<1>/\g<2>.\g<3>" ),
	( re.compile( "^/updates/(news|screen|thumbs|medium|web)/([a-z0-9-_]+)\.(jpg|tif)$" ), "/static/archives/annoucements/\g<1>/\g<2>.\g<3>" ),
	( re.compile( "^/goodies/posters/(news|screen|thumbs|medium|web)/([a-z0-9-_]+)\.(jpg|tif)$" ), "/static/archives/posters/\g<1>/\g<2>.\g<3>" ),	
]

filesredirectpatterns = [
	( re.compile( "^/goodies/(.+)" ), "/static/extras/\g<1>" ),
	( re.compile( "(.+)" ), "/static\g<1>" ),
]

link_replacements = {
	'/bin/videos.pl?searchtype=news' : '/videos/' ,
	'/bin/brochures.pl' : '/about/further_information/brochures/',
	'/bin/conferenceposters.pl' : '/about_us/conference_posters/',
	'/bin/embargo.pl' : '/public/news/archive/embargo/',
	'/bin/exhibitions.pl' : '/projects/exhibitions/',
	'/bin/fitsimages.pl' : '/projects/fits_liberator/fitsimages/',
	'/bin/images.pl' : '/images/',
	'/bin/logos.pl' : '/about_us/logos/',
	'/bin/posters.pl' : '/goodies/posters/',
	'/bin/presentations.pl' : '/goodies/presentations/',
	'/bin/slideshows.pl' : '/goodies/slideshows/',
	'/videos/index.html' : '/videos/',
	'/videos' : '/videos/',
	#'/videos/hubblecast.html' : '/videos/hubblecast/',
	'/projects/contact.html' : '/contact/',
	'/about/about/history/launch_1990.html' : '/about/about/history/launch_1990/',
	'/about/about/history/servicing_mission_1.html' : '/about/history/servicing_mission_1/',
	'/about/about/history/servicing_mission_2.html' : '/about/history/servicing_mission_2/',
	'/about/about/history/servicing_mission_3a.html' : '/about/history/servicing_mission_3a/',
	'/about/about/history/servicing_mission_3b.html' : '/about/history/servicing_mission_3b/',
	'//contact.html' : '/contact/',
	'/about/videos/index.html' : '/videos/',
	'/hubbleshop/secure_payments.htm' : '/shop/secure_payments/',
	'/projects/fits_liberator/v23files/releasenotes.html' : '/static/projects/fits_liberator/v23files/releasenotes.html',
	'/images/archive/topic/cosmo//' : '/images/archive/category/cosmology/',
	'/images/archive/topic/galax//' : '/images/archive/category/galaxies/',
	'/images/archive/topic/illustration//' : '/images/archive/category/illustrations/',
	'/images/archive/topic/illustration/viewall/' : '/images/archive/category/illustrations/',
	'/images/archive/topic/jwst//' : '/images/archive/category/jwst/',
	'/images/archive/topic/misc//' : '/images/archive/category/misc/',
	'/images/archive/topic/mission//' : '/images/archive/category/mission/',
	'/images/archive/topic/nebula//' : '/images/archive/category/nebulae/',
	'/images/archive/topic/quasar//' : '/images/archive/category/quasars/',
	'/images/archive/topic/solar+system//' : '/images/archive/category/solarsystem/',
	'/images/archive/topic/spacecraft//' : '/images/archive/category/spacecraft/',
	'/images/archive/topic/star+cluster//' : '/images/archive/category/starclusters/',
	'/images/archive/topic/star//' : '/images/archive/category/stars/',
	'/images/archive/viewall/' : '/images/',
	'/bin/calendar.pl?string=2008' : '/goodies/calendar/',
	'/bin/images.pl?embargo=0&viewtype=standard&searchtype=freesearch&lang=en&string=Deep+Field' : '/images/?search=%22Deep+Field%22',
	'/bin/images.pl?viewtype=&searchtype=freesearch&string=9914' : '/images/?search=9914',
	'/bin/news.pl?embargo=0&viewtype=standard&searchtype=freesearch&lang=en&string=proto-planetary+nebulae' : '/news/?search=%2Bproto-planetary+%2Bnebulae',
	'/bin/updates.pl?viewtype=viewall&searchtype=year&string=2008&from=1&lang=en' : '/announcements/archive/year/2008/',
	'/bin/videos.pl?embargo=0&viewtype=standard&searchtype=freesearch&lang=en&string=Deep+Field' : '/videos/?search=%22Deep+Field%22',
	'/bin/videos.pl?viewtype=&searchtype=freesearch&string=15+years+of+discovery' : '/videos/?search=%2215+years+of+discovery%22',
	'/projects/web' : '/projects/web/',
	'/projects/fits_liberator' : '/projects/fits_liberator/',
	#'/projects/fits_liberator/bugs' : 'http://www.djangoplicity.org/bugs/',
	'/news' : '/news/',
	'/kidsandteachers' : '/kidsandteachers/',
	'/images/archive/freesearch/quasar/viewall/1' : '',
	'/images/archive/topic/illustration/viewall/1' : '',
	'/images' : '/images/',
	'/about_us' : '/about_us/',
	'/goodies/slideshows/hubble_images_1.swf' : '/static/archives/slideshows/flash/hubble_images_1.swf',
	'/pressroom' : '/pressroom/',
	'/projects/anniversary/' : '/projects/anniversary/',
	#'/bin/mailform/majordomo@eso.org/hubblenews' : '/bin/mailform/majordomo@eso.org/hubblenews',
	#'/about/history/sm4blog/' : '',
	#'/hubbleshop/webshop/webshop.php?show=sales&section=books' : '',
	#'/hubbleshop/webshop/webshop.php?show=sales&section=brochures' : '',
	#'/hubbleshop/webshop/webshop.php?show=sales&section=cdroms' : '',
	#'/hubbleshop/webshop/webshop.php?show=sales&section=merchandise' : '',
	#'/hubbleshop/webshop/webshop.php?show=sales&section=newsletters' : '',
	#'/hubbleshop/webshop/webshop.php?show=sales&section=postcards' : '',
	#'/hubbleshop/webshop/webshop.php?show=sales&section=stickers' : '',
	#'/hubbleshop/webshop/webshop.php?show=sales&section=techdocs' : '',
#	'/projects/seminars/presentations/roth_art.pdf' : '/projects/seminars/presentations/roth_art.pdf',
#	'/q/spacemailform.php' : '',	
}

# Additional Redirects
# /internal/todo/.* -> http:/www.djangoplicity.org/todo/
# /bugs/.* -> http:/www.djangoplicity.org/bugs/
# /recaptcha -> /static/recaptcha
#

def choose_tasks():
	return pagestasks

#
# Define migration tasks
#
archivetasks = [
	# INIT
	ArchiveInitializationTask( Redirect ),
	
	
	ArchiveInitializationTask( Release ),
	ArchiveInitializationTask( Image ),
    
    # Goodies
    ArchiveInitializationTask( EducationalMaterial ),
    ArchiveInitializationTask( KidsDrawing ),
    ArchiveInitializationTask( Calendar ),
# OnlineArt
# OnlineArtAuthor
# Print Layout
    ArchiveInitializationTask( SlideShow ),
    
    #Products
    ArchiveInitializationTask( Book ),
    ArchiveInitializationTask( CDROM ),
    ArchiveInitializationTask( Brochure ),
    ArchiveInitializationTask( Merchandise ),
    ArchiveInitializationTask( Newsletter ),
    ArchiveInitializationTask( PostCard ),
    ArchiveInitializationTask( Poster ),
    ArchiveInitializationTask( PressKit ),
    ArchiveInitializationTask( Sticker ),

    
    #ORG
   
   
    # MIG
    ArchiveMigrationTask( SpacetelescopeCSVDataSource( '/Volumes/webdocs/spacetelescope/docs/csvfiles/newsdata.csv'), NewsDataMapping ),
	ArchiveMigrationTask( SpacetelescopeCSVDataSource( '/Volumes/webdocs/spacetelescope/docs/csvfiles/imagedata.csv'), ImagesDataMapping ),
	
	# Goodies
	ArchiveMigrationTask( SpacetelescopeCSVDataSource( '/Users/luis/Workspaces/pttu/spacetelescope.org/migration/csvfiles/edumatdata.csv'), EducationalMaterialsDataMapping ),
	ArchiveMigrationTask( SpacetelescopeCSVDataSource( '/Users/luis/Workspaces/pttu/spacetelescope.org/migration/csvfiles/kidsdrawingdata.csv'), KidsDrawingsDataMapping ),
	ArchiveMigrationTask( SpacetelescopeCSVDataSource( '/Users/luis/Workspaces/pttu/spacetelescope.org/migration/csvfiles/calendardata.csv'), CalendarsDataMapping ),
# OnlineArt
# OnlineArtAuthor
# Print Layout

    # Products
    ArchiveMigrationTask( SpacetelescopeCSVDataSource( '/Users/luis/Workspaces/pttu/spacetelescope.org/migration/csvfiles/slideshowdata.csv'), SlideShowDataMapping ),
    ArchiveMigrationTask( SpacetelescopeCSVDataSource( '/Users/luis/Workspaces/pttu/spacetelescope.org/migration/csvfiles/bookdata.csv'), BookDataMapping ),
    ArchiveMigrationTask( SpacetelescopeCSVDataSource( '/Users/luis/Workspaces/pttu/spacetelescope.org/migration/csvfiles/cdromdata.csv'), CDROMDataMapping ),
    ArchiveMigrationTask( SpacetelescopeCSVDataSource( '/Users/luis/Workspaces/pttu/spacetelescope.org/migration/csvfiles/brochuredata.csv'), BrochureDataMapping ),
    ArchiveMigrationTask( SpacetelescopeCSVDataSource( '/Users/luis/Workspaces/pttu/spacetelescope.org/migration/csvfiles/merchandisedata.csv'), MerchandiseDataMapping ),
    ArchiveMigrationTask( SpacetelescopeCSVDataSource( '/Users/luis/Workspaces/pttu/spacetelescope.org/migration/csvfiles/newsletterdata.csv'), NewsletterDataMapping ),
    ArchiveMigrationTask( SpacetelescopeCSVDataSource( '/Users/luis/Workspaces/pttu/spacetelescope.org/migration/csvfiles/postcarddata.csv'), PostCardDataMapping ),
    ArchiveMigrationTask( SpacetelescopeCSVDataSource( '/Users/luis/Workspaces/pttu/spacetelescope.org/migration/csvfiles/posterdata.csv'), PosterDataMapping ),
    ArchiveMigrationTask( SpacetelescopeCSVDataSource( '/Users/luis/Workspaces/pttu/spacetelescope.org/migration/csvfiles/presskitdata.csv'), PressKitDataMapping ),
    ArchiveMigrationTask( SpacetelescopeCSVDataSource( '/Users/luis/Workspaces/pttu/spacetelescope.org/migration/csvfiles/stickerdata.csv'), StickerDataMapping ),
    
    # Org
    #ArchiveMigrationTask( SpacetelescopeCSVDataSource( '/Users/luis/Workspaces/pttu/spacetelescope.org/migration/csvfiles/updatedata.csv'), AnnouncementDataMapping ),
    #ArchiveMigrationTask( SpacetelescopeCSVDataSource( '/Users/luis/Workspaces/pttu/spacetelescope.org/migration/csvfiles/conferenceposterdata.csv'), ConferencePosterDataMapping ),
    #ArchiveMigrationTask( SpacetelescopeCSVDataSource( '/Users/luis/Workspaces/pttu/spacetelescope.org/migration/csvfiles/logodata.csv'), LogoDataMapping ),
    #ArchiveMigrationTask( SpacetelescopeCSVDataSource( '/Users/luis/Workspaces/pttu/spacetelescope.org/migration/csvfiles/techdocsdata.csv'), TechnicalDocumentDataMapping ),
    
]

#
# Command to extract list of pages to migrate:
# find . | grep -E '\.(html|htm)$' | grep -v /html/ | grep -v -E '^\./(about/history/sm4blog/|bin/|bugs/|goodies/slideshows/flash/|goodies/mergingGalaxiesSite/|error_401.html$|pressroom/error_401.html$|error_404.html$|nvff/|projects/fits_liberator/bugs/|projects/python-xmp-toolkit/|q/|search/|xmm/|internal/|sitemap.html$|index.html$|internal_old/|testphp/|mn/|googlea95441ee32fbe5c8.html$|googlead94a0599adf8109.html$|index_test.html$|maptest/|tests/|unavailable.html$|test/|google34e371fb40a60c65.html$|images/search2.html$|integral/|netscape.html$|pressroom/embargo/index.html$|projects/web/article2.html$|projects/anniversary/index2.html$|goodies/interactive_hubble/index_old.html$|projects/fits_liberator/v23files/releasenotes.html$|images/zoom/Template.htm$|projects/av_lab/Summary of Interviews_files/header.htm$|projects/av_lab/Summary of Interviews.htm$|projects/credibility/Summary of Interviews_files/header.htm$|projects/credibility/Summary%20of%20Interviews.htm$|iyalogos.htm$|pressroom/presskits/index.html$)'
#
pagestasks = [
	PageInitializationTask(),
	PageMigrationTask( SpacetelescopePageDocument( 'about/further_information/presskits/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/further_information/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/further_information/links.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/further_information/literature.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/further_information/litterature.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/costar.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/acs.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/ghrs.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/fgs.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/foc.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/fos.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/hsp.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/nicmos.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/stis.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/wfpc1.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/wfpc2.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/wfc3.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/cos.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/wfc3_new.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/cos_new.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/fgs_new.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/cos_old.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/fgs_old.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/instruments/wfc3_old.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/electrical_systems.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/fact_sheet.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/gyroscopes.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/institutions.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/old_solar_panels.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/operations.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/orbit.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/solar_panels.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/spacecraft.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/gyroscopes_new.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/batteries_new.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/soft capture_new.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/batteries.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/gyroscopes_old.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/general/soft_capture.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/future_servicing_missions.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/aberration_problem.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/servicing_mission_3a.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/launch_1990.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/servicing_mission_1.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/servicing_mission_2.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/servicing_mission_3b.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm3a_live_coverage.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm3a_update1.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm3a_update10.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm3a_update11.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm3a_update12.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm3a_update2.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm3a_update3.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm3a_update4.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm3a_update5.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm3a_update6.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm3a_update7.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm3a_update8.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm3a_update9.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm3b_a_little_boost.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm3b_a_new_coat.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm3b_astronauts.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm3b_new_solar_panels.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm3b_nicmos_returns.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm3b_replacement_of_pcu.htm' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/the_man_behind_the_name.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/timeline.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/servicing_mission_4.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/trivia_2008.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/servicing_mission_4_new.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/stis_repair.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/acs_repair.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/esa.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/Tools_new.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/Crew_new.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/IMAX_new.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/thermal_new.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/servicing_mission_4_old.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/imax.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/tools.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/thermal.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/crew.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm4_timeline.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/sm4_tv.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/history/timeline_test.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/glossary.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/faq.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about_us/evaluation/google_news.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about_us/evaluation/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about_us/evaluation/press_clippings.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about_us/evaluation/web_stats.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about_us/heic/european.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about_us/heic/group.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about_us/heic/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about_us/heic/mission.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about_us/heic/products.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about_us/heic/scientist_guidelines.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about_us/heic/students.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about_us/heic/world.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about_us/contact.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about_us/copyright.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about_us/hubblenews.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'about_us/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'goodies/art/submit_art.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'goodies/image_experience/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'goodies/interactive_hubble/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'goodies/slideshows/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'goodies/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'goodies/orbit.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'goodies/tutorial/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'goodies/tutorial/index1.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'goodies/slideshows.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'goodies/ecards/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'goodies/ecards/xmas2006/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'hubbleshop/cvc_info.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'hubbleshop/freeorders.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'hubbleshop/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'hubbleshop/maintenance.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'hubbleshop/payment.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'hubbleshop/purchasing_steps.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'hubbleshop/secure_payments.htm' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'hubbleshop/shipping.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'hubbleshop/terms_conditions.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'hubbleshop/bulk_orders.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'contact.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'copyright.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'images/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'images/search.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'kidsandteachers/exercises.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'kidsandteachers/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'kidsandteachers/submit_drawings.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'pressroom/crabfacts.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'pressroom/interview_possibilities.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'pressroom/broadcast_videos.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'pressroom/image_formats.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'pressroom/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'pressroom/template.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'pressroom/video_formats.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'pressroom/mailinglist.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'pressroom/presscoverage.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/DVD/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/IAU_WG/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/anniversary/about_bob.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/anniversary/about_lars.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/anniversary/about_martin.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/anniversary/anniversary.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/anniversary/educational_material.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/anniversary/book.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/anniversary/credits.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/anniversary/events.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/anniversary/events2.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/anniversary/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/anniversary/movie_dvd.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/anniversary/outlets.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/anniversary/partners.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/anniversary/planeratirum_show.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/anniversary/planetaria.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/anniversary/planetarium_show.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/anniversary/poster.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/anniversary/press_meetings.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/anniversary/soundtrack.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/av_lab/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/credibility/Summary of Interviews.htm' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/credibility/credibility.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/credibility/credibility_interviews.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/denmark/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/archives.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/blackwhitehelp.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/bugform.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/bugthanks.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/datasets.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/datateachers.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/download.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/download_v1.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/download_v2.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/eagledata.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/faq.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/fitsforeducation.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/fitsmailinglist.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/improc.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/knownissues.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/m12data.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/m17data.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/m31data.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/m35data.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/m42data.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/n11bdata.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/news.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/ngc1068data.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/ngc1569data.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/ngc5307data.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/ngc6302data.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/ngc6309data.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/ngc6652data.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/ngc6881data.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/roberts22data.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/robertsdata.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/specs.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/stepbystep.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/submit_images.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/teachersdata.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/userguide.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/userguide_v1.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/userimages.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/venusdata.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/index21.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/download_v21.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/download_v20.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/readme.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/readme21.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/index1.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/indexol.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/antennaedata.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/downloads_page.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/datasets_archives.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/knownissues_faq.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/download_v22.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/mosaicator.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/documents.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/fits_liberator/download_v23.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/cap2005.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/vo_images/improc.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/vo_images/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/web/article.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/web/download.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/web/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/kiosk.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/iauga2006.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/seminars/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/socialnetworking/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/iau_pressoffice/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/20anniversary/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/20anniversary/submissionform.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/20anniversary/submissionform_old.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'projects/20anniversary/submissionform_test.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'science/composition_of_universe.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'science/age_size.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'science/black_holes.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'science/gravitational_lensing.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'science/deep_fields.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'science/europe_hubble.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'science/formation_of_stars.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'science/index.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'science/our_solar_system.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'science/stellar_evolution.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'science/protoplanetary_extrasolar.html' ) ),
	PageMigrationTask( SpacetelescopePageDocument( 'jobs/index.html' ) ),
	SpacetelescopePageFilesCopyTask( bases=['www.spacetelescope.org','spacetelescope.org'], patterns=filesredirectpatterns ),
	SpacetelescopePageLinksCleanupTask( bases=['www.spacetelescope.org','spacetelescope.org'], patterns=redirectpatterns, link_replacements=link_replacements ),
]

tasks = choose_tasks()

if __name__ == "__main__":
	"""
	Run complete migration 
	"""
	run_migration( conf, tasks )