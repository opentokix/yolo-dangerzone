#!/usr/bin/env python3
"""
This script send a document to victoria logs, that you can use in grafana as annotations. 
With the victorialogs datasource you can use the annotations in your grafana dashboard.
""" 
import requests
import json
import click
import logging
from datetime import datetime


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()


@click.command()
@click.option('--invoker', envvar="INVOKER", type=str, required=True, help="Who triggered this command")
@click.option('--tags', envvar="TAGS", type=str, required=False, default=None, help="List of tags for the annotation")
@click.option('--message', envvar="MESSAGE", type=str, required=True, help="The message for the annotation")
@click.option('--token', '-u', envvar="TOKEN", type=str, required=False, help="User for elastic search")
@click.option('--host', '-H', envvar="HOST", type=str, required=True, default='localhost', help="Host of victorialogs server")
@click.option('--port', '-P', envvar="PORT", type=str, required=False, default='443', help="port of victorialogs server")
@click.option('--scheme', envvar="SCHEME", default='https', type=click.Choice(['http', 'https']), help="Use http or https")
def main(invoker, tags, message, token, host, port, scheme):
    if tags:
        split_tags = tags.split(',')
    uri = f"{scheme}://{host}:{port}/insert/jsonline"
    headers = {
        "Content-Type": "application/stream+json",
        "Authorization": f"Bearer {token}"
    }
    doc = {"other":
           {"level": "info",
            "invoker": invoker},
           "date": "0",
           "stream": "annotations",
           "_msg": message,
           "tags": tags}
    try:
        response = requests.post(uri, headers=headers, data=json.dumps(doc))
        response.raise_for_status()
        logger.info(f"Log sent successfully: {response.status_code}")
    except Exception as e:
        logger.error(f"Error sending log: {e}")
        exit(1)


if __name__ == "__main__":
    main(auto_envvar_prefix='ANNOTATION')
