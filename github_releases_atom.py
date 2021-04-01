#!/usr/bin/python3
import feedparser

def table_printer(data):
    for d in data.keys():
        print("{0:<15} {1:<10}".format(d, data[d][1]))

def main():
    data = {"promerium": [ "https://github.com/pomerium/pomerium/releases.atom", None ],
            "grafana": ["https://github.com/grafana/grafana/releases.atom", None],
            "xsecurelock": ["https://github.com/google/xsecurelock/releases.atom", None] 
            }
    for d in data.keys():
        p = feedparser.parse(data[d][0])
        data[d][1] = p.entries[0]['title']
    table_printer(data)
if __name__ == '__main__':
    main()
