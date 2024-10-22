import click
import requests
import json
import os
from typing import Optional

class UpCloudAPI:
    def __init__(self, username: str, password: str):
        self.base_url = "https://api.upcloud.com/1.3"
        self.auth = (username, password)
        self.headers = {
            "Content-Type": "application/json"
        }

    def _make_request(self, method: str, endpoint: str, data: Optional[dict] = None) -> dict:
        url = f"{self.base_url}/{endpoint}"
        response = requests.request(
            method=method,
            url=url,
            auth=self.auth,
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()

    def list_servers(self) -> dict:
        return self._make_request("GET", "server")

    def create_server(self, server_data: dict) -> dict:
        return self._make_request("POST", "server", data={"server": server_data})

    def delete_server(self, uuid: str) -> None:
        return self._make_request("DELETE", f"server/{uuid}")

def get_api_client():
    username = os.environ.get("UPCLOUD_USERNAME")
    password = os.environ.get("UPCLOUD_PASSWORD")

    if not username or not password:
        raise click.ClickException(
            "UPCLOUD_USERNAME and UPCLOUD_PASSWORD environment variables must be set"
        )

    return UpCloudAPI(username, password)

@click.group()
def cli():
    """UpCloud CLI tool for managing servers"""
    pass

@cli.command()
@click.option('--hostname', required=True, help='Hostname for the server')
@click.option('--plan', default='1xCPU-1GB', help='Server plan (e.g., 1xCPU-1GB)')
@click.option('--zone', default='fi-hel1', help='Zone where server will be created')
@click.option('--disk-size', default=25, type=int, help='Size of the disk in GB')
@click.option('--disk-tier', default='maxiops', type=click.Choice(['maxiops', 'hdd']), help='Disk tier')
@click.option('--backup/--no-backup', default=False, help='Enable automatic backups')
@click.option('--backup-time', default='0000', help='Backup time in HHMM format')
@click.option('--backup-interval', default='daily', type=click.Choice(['daily', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']),
              help='Backup interval')
@click.option('--network-private/--no-network-private', default=False, help='Add private network')
def create(hostname, plan, zone, disk_size, disk_tier, backup, backup_time, backup_interval, network_private):
    """Create a new server"""
    try:
        client = get_api_client()

        server_data = {
            "hostname": hostname,
            "plan": plan,
            "zone": zone,
            "title": hostname,
            "storage_devices": {
                "storage_device": [{
                    "action": "clone",
                    "storage": "01000000-0000-4000-8000-000030200200",  # Ubuntu 20.04 template
                    "title": f"{hostname}-disk",
                    "size": disk_size,
                    "tier": disk_tier
                }]
            }
        }

        if backup:
            server_data["backup_rule"] = {
                "interval": backup_interval,
                "time": backup_time,
                "retention": 7
            }

        if network_private:
            server_data["networking"] = {
                "interfaces": [
                    {
                        "ip_addresses": [{"family": "IPv4", "address": "auto"}],
                        "type": "public"
                    },
                    {
                        "ip_addresses": [{"family": "IPv4", "address": "auto"}],
                        "type": "private"
                    }
                ]
            }

        result = client.create_server(server_data)
        click.echo(f"Server created successfully: {json.dumps(result, indent=2)}")

    except Exception as e:
        raise click.ClickException(str(e))

@cli.command()
def list():
    """List all servers"""
    try:
        client = get_api_client()
        servers = client.list_servers()
        click.echo(json.dumps(servers, indent=2))
    except Exception as e:
        raise click.ClickException(str(e))

@cli.command()
@click.argument('uuid')
@click.option('--force/--no-force', default=False, help='Force deletion without confirmation')
def delete(uuid, force):
    """Delete a server by UUID"""
    try:
        if not force:
            if not click.confirm(f'Are you sure you want to delete server {uuid}?'):
                return

        client = get_api_client()
        client.delete_server(uuid)
        click.echo(f"Server {uuid} deleted successfully")
    except Exception as e:
        raise click.ClickException(str(e))

if __name__ == '__main__':
    cli()
