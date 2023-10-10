#!/usr/bin/env python3
import json
import requests
import click


@click.command()
@click.option('--gitlab', envvar="GITLAB_URL", default='https://localhost', help='Gitlab server to get users from')
@click.option('--token', envvar="GITLAB_TOKEN", help='Token to authenticate with')
@click.option('--email', help="Also print email associated with account", is_flag=True, default=False)
def main(gitlab, token, email):
    """Get all users from a Gitlab server"""
    if not token:
      print("Please provide a token")
      exit(1)
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
        if user['state'] == 'blocked':
          continue
        if email:
          print(f"{user['name']}, {user['username']}, {user['email']}")
        else:
          print(f"{user['name']}")


if __name__ == '__main__':
    main()

