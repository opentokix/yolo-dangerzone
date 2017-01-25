#!/usr/bin/env python2

import elasticsearch
import datetime
import sys
import getopt

global SILENT
SILENT=False


def usage():
    """Generic script to post to elasticsearch.
    --host es host
    --port es port
    --index indes to use
    --tag tag to use
    --message message
    --ssl use ssl

    """
    print usage.__doc__


def post_to_es(options, timestamp):
    try:
        if options['ssl']:
            es = elasticsearch.Elasticsearch(host=options['es_host'], port=options['es_port'], use_ssl=True, verify_certs=True)
        else:
            es = elasticsearch.Elasticsearch(host=options['es_host'], port=options['es_port'])
    except:
        if SILENT is False:
            print "Elasticsearch error"
            sys.exit(1)
        else:
            sys.exit(0)
    try:
        es.index(index=options['index'], doc_type='automation',
                 body={'@timestamp': timestamp,
                       'message': options['message'],
                       'tags': options['tag']})
    except ValueError:
        if SILENT is False:
            print "Elasticsearch index error"
            sys.exit(1)
        else:
            sys.exit(0)


def main(options):
    timestamp = datetime.datetime.utcnow()
    post_to_es(options, timestamp)


def parse_options(argv):
    options = {'es_host': '127.0.0.1',
               'es_port': 9200,
               'ssl': False }
    try:
        opts, args = getopt.getopt(argv, 'qsh:p:t:i:m:', ['ssl', 'host=', 'port=', 'tag=', 'index=', 'message=', 'help', 'quite'])
    except getopt.GetoptError, e:
        print "Option error %s" % e
        sys.exit(1)
    for opt, arg in opts:
        if opt in ('help'):
            usage()
            sys.exit(0)
        elif opt in ('-h', '--host'):
            options['es_host'] = arg
        elif opt in ('-p', '--port'):
            options['es_port'] = int(arg)
        elif opt in ('-t', '--tag'):
            options['tag'] = arg
        elif opt in ('-i', '--index'):
            options['index'] = arg
        elif opt in ('-m', '--message'):
            options['message'] = arg
        elif opt in ('-q', '--quite'):
            global SILENT
            SILENT=True
        elif opt in ['-s', '--ssl']:
            options['ssl'] = True

    if 'message' not in options:
        print "Message is mandatory option"
        usage()
        sys.exit(1)
    if 'index' not in options:
        print "Index is mandatory option"
        usage()
        sys.exit(1)
    if 'tag' not in options:
        print "Tag is mandatory option"
        usage()
        sys.exit(1)
    main(options)

if __name__ == '__main__':
    parse_options(sys.argv[1:])
