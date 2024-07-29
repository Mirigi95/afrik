import ccxt
import time

# Initialize exchanges
exchanges = [
    ccxt.binance(),  # Binance
    ccxt.kraken(),   # Kraken
    ccxt.bybit(),    # Bybit
    ccxt.okx(),      # OKX
    ccxt.huobi(),    # Huobi
    ccxt.mexc()      # MEXC
]

# Fetch and store the list of symbols/markets for each exchange
symbols_per_exchange = {}
for exchange in exchanges:
    try:
        symbols = exchange.load_markets()
        symbols_per_exchange[exchange.id] = symbols.keys()
    except Exception as e:
        print(f"Error fetching markets from {exchange.id}: {e}")

# Find the intersection of symbols across all exchanges
common_symbols = set(symbols_per_exchange[exchanges[0].id])
for exchange_id, symbols in symbols_per_exchange.items():
    common_symbols.intersection_update(symbols)

# Initialize a dictionary to store prices for common symbols
common_symbol_prices = {symbol: {} for symbol in common_symbols}

# Fetch prices for common symbols from each exchange
for exchange in exchanges:
    for symbol in common_symbols:
        try:
            ticker = exchange.fetch_ticker(symbol)
            common_symbol_prices[symbol][exchange.id] = ticker['last']
        except Exception as e:
            print(f"Error fetching ticker for {symbol} from {exchange.id}: {e}")

# Check for arbitrage opportunities with price differences above 1%
print("Arbitrage opportunities with price differences above 0.5%:")
for symbol, prices in common_symbol_prices.items():
    exchange_prices = list(prices.items())
    for i in range(len(exchange_prices)):
        for j in range(i + 1, len(exchange_prices)):
            exchange1, price1 = exchange_prices[i]
            exchange2, price2 = exchange_prices[j]
            if price1 is not None and price2 is not None:
                price_difference = abs(price1 - price2)
                percentage_difference = (price_difference / ((price1 + price2) / 2)) * 100
                if percentage_difference > 0.5:
                    print(f"{symbol}:")
                    print(f"  {exchange1}: {price1}")
                    print(f"  {exchange2}: {price2}")
                    print(f"  Percentage difference: {percentage_difference:.2f}%")

time.sleep(300) 
