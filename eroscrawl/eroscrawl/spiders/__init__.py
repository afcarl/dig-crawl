# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import sys, os, datetime, errno
import logging
from scrapy.log import ScrapyFileLogObserver

try:
    import sys, os, datetime, errno
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
    logfile = open(os.path.join(logdir, "scrapy.log"), 'a')
    log_observer = ScrapyFileLogObserver(logfile, level=logging.DEBUG)
    log_observer.start()

except Exception as e:
    print >> sys.stderr, "Failed to create log dir %r [%r]" % (logdir, e)

import sys
print >> sys.stderr, "SETTINGS: log file %r" % logfile
