#!/usr/bin/env python3
import click
import json
import subprocess
import sys
import shutil
from dotenv import dotenv_values

def check_op_installed():
    """Checks if the 'op' CLI is installed and accessible."""
    if not shutil.which("op"):
        click.secho("Error: The 'op' CLI command was not found. Please install the 1Password CLI.", fg="red", err=True)
        sys.exit(1)

def get_env_secrets(file_path):
    """Reads the .env file and returns a dictionary of key/values."""
    try:
        # dotenv_values parses the file without loading it into environment variables
        config = dotenv_values(file_path)

        # Filter out any None values (which can happen if parsing fails for a line)
        clean_config = {k: v for k, v in config.items() if k is not None and v is not None}
        return clean_config

    except Exception as e:
        click.secho(f"Error parsing .env file: {e}", fg="red", err=True)
        sys.exit(1)

def item_exists(vault, item_name):
    """Checks if an item exists in the specified vault."""
    result = subprocess.run(
        ["op", "item", "get", item_name, "--vault", vault],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    return result.returncode == 0

def create_1password_item(vault, item_name, secrets):
    """Constructs a JSON template and pipes it to `op item create`."""

    fields = []

    # 1. Add Default/Placeholder Fields (Required for 'Password' Category)
    fields.append({
        "id": "username",
        "label": "username",
        "value": "not-used",
        "type": "STRING"
    })

    fields.append({
        "id": "password",
        "label": "password",
        "value": "not-used",
        "purpose": "PASSWORD",
        "type": "CONCEALED"
    })

    # 2. Add ALL env vars as additional fields
    for key, value in secrets.items():
        fields.append({
            "label": key,
            "value": value,
            "type": "CONCEALED"
        })

    item_template = {
        "title": item_name,
        "fields": fields
    }

    json_payload = json.dumps(item_template)

    try:
        process = subprocess.run(
            ["op", "item", "create", "-", "--vault", vault, "--category", "Password"],
            input=json_payload,
            text=True,
            capture_output=True
        )

        if process.returncode != 0:
            click.secho(f"Error creating item: {process.stderr}", fg="red", err=True)
            sys.exit(1)

        click.secho(f"Successfully created item '{item_name}' (Category: Password) in vault '{vault}'.", fg="green")

    except Exception as e:
        click.secho(f"System error invoking op CLI: {e}", fg="red", err=True)
        sys.exit(1)

def delete_item(vault, item_name):
    """Deletes an item."""
    click.echo(f"Overwriting: Deleting existing item '{item_name}'...")
    subprocess.run(
        ["op", "item", "delete", item_name, "--vault", vault],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )

@click.command()
@click.option('--env-file', required=True, type=click.Path(exists=True), help='Path to the .env file.')
@click.option('--vault', required=True, help='The name of the 1Password Vault.')
@click.option('--item-name', required=True, help='The name of the item to create in 1Password.')
@click.option('--force', is_flag=True, help='Overwrite the item if it already exists.')
@click.option('--dry-run', is_flag=True, help='Simulate the output without changing data.')
def main(env_file, vault, item_name, force, dry_run):
    """
    Reads an .env file and pushes the key/values to 1Password.
    """
    check_op_installed()

    if dry_run:
        click.secho(f"--- DRY RUN MODE ---", fg="cyan", bold=True)

    click.echo(f"Reading secrets from {env_file}...")
    secrets = get_env_secrets(env_file)

    if not secrets:
        click.secho("No data found in the .env file.", fg="yellow")
        sys.exit(0)

    exists = item_exists(vault, item_name)

    if exists:
        if force:
            if dry_run:
                click.secho(f"[Dry Run] Item '{item_name}' exists in '{vault}'. It WOULD be deleted.", fg="yellow")
            else:
                delete_item(vault, item_name)
        else:
            msg = f"Item '{item_name}' already exists in vault '{vault}'. Use --force to overwrite."
            if dry_run:
                click.secho(f"[Dry Run] {msg}", fg="red")
            else:
                click.secho(msg, fg="red", err=True)
                sys.exit(1)

    if dry_run:
        click.secho(f"\n[Dry Run] Would create item '{item_name}' (Category: Password) in vault '{vault}'.", fg="cyan")
        click.echo("-" * 40)

        click.secho("DEFAULT FIELDS (Fixed):", fg="green")
        click.echo("username: not-used")
        click.echo("password: not-used (purpose: PASSWORD)")
        click.echo("-" * 20)

        click.secho(f"IMPORTED FIELDS ({len(secrets)}):", fg="green")
        for k, v in secrets.items():
             click.echo(f"{k}: {v} (Type: CONCEALED)")

        click.echo("-" * 40)
        click.secho("[Dry Run] Complete.", fg="cyan")
    else:
        if exists and not force:
             return

        click.echo(f"Creating item '{item_name}' with {len(secrets)} imported fields...")
        create_1password_item(vault, item_name, secrets)

if __name__ == '__main__':
    main()
