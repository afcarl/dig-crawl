# -*- coding: utf-8 -*-

# Scrapy settings for eroscrawl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'eroscrawl'

SPIDER_MODULES = ['eroscrawl.spiders']
NEWSPIDER_MODULE = 'eroscrawl.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'eroscrawl (+http://www.yourdomain.com)'

# 13 October 2014
DOWNLOAD_DELAY = 1.0

# 5 November 2014
LOG_LEVEL = 'INFO'

# data dir
try:
    import sys, os, datetime, errno, time
    today = datetime.datetime.utcnow().strftime("%Y%m%d")
    datadir = None
    # ACCUM is the root directory
    try:
        accum = os.environ["ACCUM"]
    except:
        accum = "/lfs1/users/wat"
    datadir = os.path.join(accum, "data/escort/%s/www.eros.com/" % today)
    # ensure data directory exists
    try:
        os.makedirs(datadir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    datafile = os.path.join(datadir, "scrapy.json")
    # if datafile already exists, try to rename
    try: 
        os.rename(datafile, "%s.%s" % (datafile, time.time()))
    except:
        # if possible
        pass
    feed_uri = "file://" + datafile
    # ensure images subdirectory exists
    images_store = os.path.join(datadir, "images")
    try:
        os.makedirs(images_store)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
except Exception as e:
    print >> sys.stderr, "Failed to configure data dir %r [%r]" % (datadir, e)

ITEM_PIPELINES = {'scrapy.contrib.pipeline.images.ImagesPipeline': 1}
IMAGES_STORE = images_store

# FEED_URI = "file:///lfs1/users/wat/data/escort/scrapy/%(time)s.json"
FEED_URI = feed_uri
FEED_FORMAT = "jsonlines"

# log dir
try:
    import sys, os, datetime, errno, time
    today = datetime.datetime.utcnow().strftime("%Y%m%d")
    logdir = None
    # ACCUM is the root directory
    try:
        accum = os.environ["ACCUM"]
    except:
        accum = "/lfs1/users/wat"
    logdir = os.path.join(accum, "log/escort/%s/www.eros.com/" % today)
    # ensure log directory exists
    try:
        os.makedirs(logdir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
    logfile = os.path.join(logdir, "log")
    # if logfile already exists, try to rename
    try: 
        os.rename(logfile, "%s.%s" % (logfile, time.time()))
    except:
        # if possible
        pass
except Exception as e:
    print >> sys.stderr, "Failed to configure log dir %r [%r]" % (logdir, e)

LOG_FILE = logfile

# dump all to stdout/log?
import sys
print >> sys.stderr, "SETTINGS: Feed URI %r" % FEED_URI
print >> sys.stderr, "SETTINGS: Images store %r" % IMAGES_STORE
print >> sys.stderr, "SETTINGS: Log file %r" % LOG_FILE
