#!/usr/bin/env python3
import json
import requests
import click


@click.command()
@click.option('--gitlab', default='https://localhost', help='Gitlab server to get users from')
@click.option('--token', help='Token to authenticate with')
def main(gitlab, token):
    """Get all users from a Gitlab server"""
    url = f"{gitlab}/api/v4/users?private_token={token}"
    response = requests.get(url)
    pages = response.headers['X-Total-Pages']
    for page in range(1, int(pages) + 1):
      url = f"{gitlab}/api/v4/users?private_token={token}&page={page}"
      response = requests.get(url)
      users = response.json()
      for user in users:
        if user['bot']:
          continue
        if user['state'] != 'active':
          continue
        print(f"{user['name']}")

if __name__ == '__main__':
    main()

