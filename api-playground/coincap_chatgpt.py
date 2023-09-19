import click
import requests

COINCAP_URL = "https://api.coincap.io/v2/assets/"

@click.command()
@click.argument("ticker")
def get_crypto_price(ticker):
    """Fetch the current price of the given cryptocurrency ticker in USD from CoinCap API."""
    try:
        response = requests.get(COINCAP_URL + ticker)
        response.raise_for_status()

        data = response.json()
        if "data" in data:
            price_usd = data["data"]["priceUsd"]
            click.echo(f"The current price of {ticker.upper()} in USD is: ${price_usd}")
        else:
            click.echo(f"Error: {data['error']}")
    except requests.RequestException as error:
        click.echo(f"Error fetching data: {error}")

if __name__ == "__main__":
    get_crypto_price()
