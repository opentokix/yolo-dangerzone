#!/usr/bin/env python2

import logging
import logstash

def main():
    test_logger = logging.getLogger('python-logstash-logger')
    test_logger.setLevel(logging.INFO)
    test_logger.addHandler(logstash.TCPLogstashHandler(host='172.16.135.1', port=5050, version=1))
    test_logger.info('python-logstash: test logstash info message.')
    try:
        1/0
    except:
        test_logger.exception('python-logstash-logger: Exception with stack trace!')




if __name__  == '__main__':
    main()
