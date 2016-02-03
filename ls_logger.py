#!/usr/bin/env python2

import logging
import logstash

def main():
    test_logger = logging.getLogger('python-logstash-logger')
    test_logger.setLevel(logging.INFO)
    test_logger.addHandler(logstash.TCPLogstashHandler(host='172.17.0.2', port=5050, version=1))
    test_logger.info('python-logstash: test logstash info message.')

    s_logger = logging.getLogger('python-syslog-logger')
    s_logger.setLevel(logging.INFO)
    s_handler = logging.handlers.SysLogHandler(address=('172.17.0.2', 5000),facility=19)
    s_logger.addHandler(s_handler)
    s_logger.info('python-syslog: test logstash info message.')

    try:
        1/0
    except:
        test_logger.exception('python-logstash-logger: Exception with stack trace!')
        s_logger.exception('python-syslog-loggger: Exception wwwith stack trace!')



if __name__  == '__main__':
    main()
