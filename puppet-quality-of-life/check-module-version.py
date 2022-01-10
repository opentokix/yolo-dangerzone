#!/usr/bin/python3

import click
import logging
import json
from urllib.request import urlopen

logger = logging.getLogger('forgetool')
logger.setLevel(logging.ERROR)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)

def get_module_latest(name, forge):
    url = f"{forge}/v3/modules/{name}"
    try:
        response = urlopen(url)
    except Exception as e:
        logger.error(f"{url} did not work with {e}")
    try:
        data_json = json.loads(response.read())
    except Exception as e:
        logger.error(f"Probelem with json: {e}")
        exit(1)
    data = data_json['current_release']['version']
    return data

@click.command()
@click.option('--name', '-N', required=True, default=None, help="The module you want version of")
@click.option('--forge', '-F', required=False, default="https://forgeapi-cdn.puppet.com", help="Forge url")
@click.option('--all', '-A', is_flag=True, default=False, help="List all version of the module")
def main(name, forge, all):
    if not all:
        d = get_module_latest(name, forge)
        print(d)
    else:
        logger.error("All flag is not implemented yet")
        exit(1)

if __name__ == '__main__':
    main()
