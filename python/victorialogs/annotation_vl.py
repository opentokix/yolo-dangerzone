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
@click.option('--invoker', envvar="INVOKER", type=str, required=True, help="Who triggered this command")  # noqa E501
@click.option('--tags', envvar="TAGS", type=str, required=False, default=None, help="List of tags for the annotation")  # noqa E501
@click.option('--message', envvar="MESSAGE", type=str, required=True, help="The message for the annotation")  # noqa E501
@click.option('--token', '-u', envvar="TOKEN", type=str, required=False, help="User for elastic search")  # noqa E501
@click.option('--type_of', "-T", envvar="TYPE", required=True, type=click.Choice(['warning', 'ok', 'error', 'information', 'critical']), help="Type of the annotation")  # noqa E501
@click.option('--system', '-s', envvar="SYSTEM", type=str, required=False, default="undefined", help="System for elastic search")  # noqa E501  # noqa E501
@click.option('--host', '-H', envvar="HOST", type=str, required=True, default='localhost', help="Host of victorialogs server")  # noqa E501
@click.option('--port', '-P', envvar="PORT", type=str, required=False, default='443', help="port of victorialogs server")  # noqa E501
@click.option('--scheme', envvar="SCHEME", default='https', type=click.Choice(['http', 'https']), help="Use http or https")  # noqa E501
def main(invoker, tags, message, token, host, port, scheme, system, type_of):
    stream_fields = "stream,level,invoker,system,type_of"
    uri = f"{scheme}://{host}:{port}/insert/jsonline?_stream_fields={stream_fields}"  # noqa E501
    headers = {
        "Content-Type": "application/stream+json",
        "Authorization": f"Bearer {token}"
    }
    doc = {"level": "info",
           "invoker": invoker,
           "system": system,
           "stream": "annotations",
           "type": type_of,
           "_msg": message,
           "tags": tags if tags else [],
           }
    try:
        response = requests.post(uri, headers=headers, data=json.dumps(doc))
        response.raise_for_status()
        logger.info(f"Log sent successfully: {response.status_code}")
    except Exception as e:
        logger.error(f"Error sending log: {e}")
        exit(1)


if __name__ == "__main__":
    main(auto_envvar_prefix='ANNOTATION')
