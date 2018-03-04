#!/usr/bin/env python2

"""Generate fake logs to syslog."""
import logging
import logging.handlers
import uuid
from time import sleep
import random
import thread
from optparse import OptionParser


def generate_info(logging):
    """Generating some info logs."""
    session = str(uuid.uuid1())
    log_lines = ['Opening session for user with session id:', 'Authenticating user session:', 'Getting profile information ', 'User logged out session id:', '[auth] Admin user logged in: ']
    for line in log_lines:
        log_output = "%s %s\n" % (line, session)
        logging.info(log_output)
        sleep(0.3)
    q = random.randint(45, 99)
    if q > 80:
        log_output = "User quota is %s %s\n" % (str(q), str(session))
        logging.warning(log_output)


def generate_error(logging):
    """Generating some error logs."""
    log_lines = ['[auth] Lost connection to user database', '[store] Error writing', '[frontend] Wrong input', '[auth] User disabled']
    for line in log_lines:
        log_output = "%s\n" % (line)
        logging.error(log_output)
        sleep(0.3)


def generate_debug(logging):
    """Generating soem debug logs."""
    for i in range(10):
        time = "%s" % (str(random.randint(123, 900)))
        log_output = "Total processing time %sms\n" % (time)
        logging.debug(log_output)
        sleep(0.3)


def main(opts):
    """Magic main."""
    rootlogger = logging.getLogger('')
    rootlogger.setLevel(logging.DEBUG)
    sockethandler = logging.handlers.SysLogHandler(address=(opts.host, int(opts.port)))
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
    sockethandler.setFormatter(formatter)
    rootlogger.addHandler(sockethandler)
    applogging = logging.getLogger('mock')
    thread.start_new_thread(generate_info, (applogging,))
    thread.start_new_thread(generate_error, (applogging,))
    thread.start_new_thread(generate_debug, (applogging,))
    while True:
        thread.start_new_thread(generate_info, (applogging,))
        thread.start_new_thread(generate_error, (applogging,))
        thread.start_new_thread(generate_debug, (applogging,))
        sleep(random.randint(1, 3))
#    while True:
#        info_log = Process(target=generate_info(logging))
#        info_log.start()
#        error_log = Process(target=generate_error(logging))
#        error_log.start()
#        debug_log = Process(target=generate_debug(logging))
#        debug_log.start()
#        info_log.join()
#        error_log.join()
#        debug_log.join()
    sockethandler.close()


if __name__ == '__main__':
    p = OptionParser()
    p.add_option("-p", "--port", dest="port", help="Port for logging", default=5555)
    p.add_option("-H", "--host", dest="host", help="Host for logging", default='localhost')
    (opts, args) = p.parse_args()
    main(opts)
