# -*- coding: utf-8 -*-
#
# webb.org
# Copyright 2010 ESO & ESA/Hubble
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#

# Feed settings for website project

class ImageFeedSettings():
    title = 'ESAWebb Images'
    link = 'https://esawebb.org/images/'
    description = """The ESAWebb Images feed showcases breathtaking images and scientific observations captured by the NASA/ESA/CSA James Webb Space Telescope. 
    Explore stunning infrared views of nebulae, star-forming regions, and isolated planetary-mass objects, 
    accompanied by detailed descriptions and insights into the latest astronomical discoveries."""
    external_feed_url = 'https://feeds.feedburner.com/esawebb/images/'


class PictureOfTheWeekFeedSettings():
    title = 'ESAWebb Picture Of The Month'
    link = 'https://esawebb.org/images/potm/'
    description = """The ESAWebb Picture of the Month feed features a carefully selected image from the NASA/ESA/CSA James Webb Space Telescope each month. 
    These images highlight stunning cosmic phenomena, from distant galaxies to intricate nebulae, 
    accompanied by expert insights into the science behind them."""
    external_feed_url = 'https://feeds.feedburner.com/esawebb/potm/'


class AnnouncementFeedSettings():
    title = 'ESAWebb Announcements'
    link = 'https://esawebb.org/announcements/'
    description = """The ESAWebb Announcements feed provides the latest news and updates about the NASA/ESA/CSA James Webb Space Telescope. 
    Stay informed about mission developments, scientific discoveries, and important project updates."""
    external_feed_url = "https://feeds.feedburner.com/esawebb/announcements/"

class VideoFeedSettings():
    title = 'ESAWebb Images'
    link = 'https://esawebb.org/videos/'
    description = """The ESAWebb Videos feed features the latest video content related to the NASA/ESA/CSA James Webb Space Telescope. 
    Explore stunning visuals, mission updates, and expert insights through engaging video materials."""
    external_feed_url = 'https://feeds.feedburner.com/esawebb/videos/'

class ReleaseFeedSettings():
    title = 'ESAWebb News Feed'
    link = 'https://esawebb.org/news/'
    description = """The ESAWebb News feed delivers the latest updates and discoveries from the NASA/ESA/CSA James Webb Space Telescope. 
    Stay informed about groundbreaking scientific findings, mission progress, and important announcements."""
    external_feed_url = 'https://feeds.feedburner.com/esawebb/news/'


class FeedRedirectSettings():
    redirects = {
        '/images/potm/feed/': PictureOfTheWeekFeedSettings.external_feed_url,
        '/news/feed/': ReleaseFeedSettings.external_feed_url,
        '/announcements/feed/': AnnouncementFeedSettings.external_feed_url,
        '/images/feed/': ImageFeedSettings.external_feed_url,
        '/videos/feed/': VideoFeedSettings.external_feed_url,
    }

    whitelist = ['FeedBurner', ]  # ,'Mozilla']
    whitelist_ips = ['134.171.', '127.0.0.1']  # must use ?bypass=1 in request


class Top100FeedSettings():
    title = 'Hubble Top 100 Images'


CATEGORY_SPECIFIC_SETTINGS = {
    'hubblecast': 'HubblecastFeedSettings',
}

FORMATS = {
    '': ( 'HD', '' ),
    'hd': ( 'HD', '' ),
    'sd': ( 'SD', '' ),
    'fullhd': ( 'Full HD', '' ),
}
