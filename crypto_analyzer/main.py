"""
CLI Entry Point
Usage: python -m crypto_analyzer.main <coin_name_or_symbol>
"""

import sys
import click
from .api import CoinGeckoAPI
from .signals import analyze_coin
from .formatter import format_analysis, format_compact, format_top_coins


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--compact', '-c', is_flag=True, help='Compact output')
def cli(ctx, compact):
    """Crypto Market Analyzer - Technical analysis for altcoins."""
    if ctx.invoked_subcommand is None:
        # Show help if no command given
        click.echo(ctx.get_help())


@cli.command()
@click.argument('coin')
@click.option('--compact', '-c', is_flag=True, help='Show compact output')
@click.option('--days', '-d', default=60, help='Historical data days (default: 60)')
def analyze(coin, compact, days):
    """Analyze a specific coin (e.g. bitcoin, solana, eth)."""
    api = CoinGeckoAPI()

    # Search for coin
    click.echo(f"🔍 Searching for '{coin}'...", err=True)
    results = api.search(coin)

    if not results:
        click.echo(f"❌ Coin '{coin}' not found. Try symbol like BTC, ETH, SOL.")
        sys.exit(1)

    coin_id = results[0]['id']
    coin_name = results[0]['name']
    coin_symbol = results[0]['symbol']

    click.echo(f"✅ Found: {coin_name} ({coin_symbol.upper()}) — analyzing...", err=True)

    try:
        result = analyze_coin(coin_id, api)
    except Exception as e:
        click.echo(f"❌ Analysis error: {e}")
        sys.exit(1)

    if 'error' in result:
        click.echo(f"❌ {result['error']}")
        sys.exit(1)

    if compact:
        click.echo(format_compact(result))
    else:
        click.echo(format_analysis(result))


@cli.command('top')
@click.option('--limit', '-n', default=10, help='Number of coins to show')
def top(limit):
    """Show top coins by market cap."""
    api = CoinGeckoAPI()
    coins = api.get_top_coins(limit=limit)
    click.echo(format_top_coins(coins, limit))


@cli.command('trending')
def trending():
    """Show trending coins."""
    api = CoinGeckoAPI()
    data = api.get_trending()

    lines = [
        "🔥 *TRENDING COINS*",
        '═' * 35,
    ]

    for item in data:
        coin = item.get('item', {})
        name = coin.get('name', '')
        symbol = coin.get('symbol', '').upper()
        rank = coin.get('market_cap_rank', '?')
        lines.append(f"{rank}. {name} ({symbol})")

    click.echo('\n'.join(lines))


# Backward compatibility: direct coin name as argument
def main():
    if len(sys.argv) > 1 and not sys.argv[1].startswith('-'):
        # Check if it's a subcommand
        subcommands = ['analyze', 'top', 'trending']
        if sys.argv[1] not in subcommands:
            # Treat as coin name for analyze
            sys.argv.insert(1, 'analyze')
    cli()


if __name__ == '__main__':
    main()
