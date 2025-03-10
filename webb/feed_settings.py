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
    external_feed_url = 'https://feeds.feedburner.com/esawebb/images/'


class PictureOfTheWeekFeedSettings():
    title = 'ESAWebb Picture Of The Month'
    link = 'https://esawebb.org/images/potm/'
    external_feed_url = 'https://feeds.feedburner.com/esawebb/potm/'


class AnnouncementFeedSettings():
    title = 'ESAWebb Announcements'
    link = 'https://esawebb.org/announcements/'
    external_feed_url = "https://feeds.feedburner.com/esawebb/announcements/"

class VideoFeedSettings():
    title = 'ESAWebb Images'
    link = 'https://esawebb.org/videos/'
    external_feed_url = 'https://feeds.feedburner.com/esawebb/videos/'

class ReleaseFeedSettings():
    title = 'ESAWebb News Feed'
    link = 'https://esawebb.org/news/'
    description = "The latest news about astronomy and the NASA/ESA Hubble Space Telescope"
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
