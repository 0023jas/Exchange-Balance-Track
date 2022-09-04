from ethereumTools import *
import pandas as pd

# Blocks a day: 6550
# EIP-1559 block number: 12965000

# First block of 2017
# 2912407 

exchange_wallets = pd.read_csv("exchangeWallets.csv")

for block in range(2912407, latestBlockNumber, 300):
    block_number_list = []
    total_balance_list = []
    largest_exchange_balance_list = []
    largest_exchange_name_list = []
    largest_exchange_dominance_list = []
    top_five_dominance_list = []
    binance_list = []
    coinbase_list = []
    ftx_exchange_list = []
    kraken_list = []
    gate_io_list = []
    kucoin_list = []
    bitfinex_list = []
    huobi_list = []
    gemini_list = []
    bitstamp_list = []
    other_list = []

    block_number = 0
    total_balance = 0
    largest_exchange_balance = 0
    largest_exchange_name = 'mt. gox'
    largest_exchange_dominance = 0
    top_five_dominance = 0
    binance = 0
    coinbase = 0
    ftx_exchange = 0
    kraken = 0
    gate_io = 0
    kucoin = 0
    bitfinex = 0
    huobi = 0
    gemini = 0
    bitstamp = 0
    other = 0

    largest_exchange_balance_dict = {}

    for exchange_address in range(len(exchange_wallets)):
        #try:
            
        # get balance
        address = exchange_wallets['Address'][exchange_address]
        wallet_address_formatted = w3.toChecksumAddress(address)
        address_balance = getAddressBalanceAtBlock(wallet_address_formatted, block)

        # get block number
        block_number = block


        # get total balance
        total_balance += address_balance


        # get binance
        if(exchange_wallets['Exchange'][exchange_address] == "Binance"):
            binance += address_balance

        # get coinbase
        elif(exchange_wallets['Exchange'][exchange_address] == "Coinbase"):
            coinbase += address_balance

        # get ftx exchange
        elif(exchange_wallets['Exchange'][exchange_address] == "FTX Exchange"):
            ftx_exchange += address_balance

        # get kraken
        elif(exchange_wallets['Exchange'][exchange_address] == "Kraken"):
            kraken += address_balance

        # get gate.io
        elif(exchange_wallets['Exchange'][exchange_address] == "Gate.io"):
            gate_io += address_balance

        # get kucoin
        elif(exchange_wallets['Exchange'][exchange_address] == "KuCoin"):
            kucoin += address_balance

        # get bitfinex
        elif(exchange_wallets['Exchange'][exchange_address] == "Bitfinex"):
            bitfinex += address_balance

        # get huobi
        elif(exchange_wallets['Exchange'][exchange_address] == "Huobi"):
            huobi += address_balance

        # get gemini
        elif(exchange_wallets['Exchange'][exchange_address] == "Gemini"):
            gemini += address_balance

        # get bitstamp
        elif(exchange_wallets['Exchange'][exchange_address] == "Bitstamp"):
            bitstamp += address_balance

        # get other
        else:
            other += address_balance

        if exchange_wallets['Exchange'][exchange_address] in largest_exchange_balance_dict:
            largest_exchange_balance_dict[exchange_wallets['Exchange'][exchange_address]] += address_balance
        else:
            largest_exchange_balance_dict[exchange_wallets['Exchange'][exchange_address]] = address_balance


    largest_exchange_balance_dict_ordered = sorted(largest_exchange_balance_dict.items(), key=lambda x: x[1], reverse=True)

    # get largest exchange balance
    largest_exchange_balance = largest_exchange_balance_dict_ordered[0][1]


    # get largest exchange name
    largest_exchange_name = largest_exchange_balance_dict_ordered[0][0]


    # get largest exchange dominance
    largest_exchange_dominance = (largest_exchange_balance / total_balance)*100


    # get top 5 dominance

    second_largest_exchange_balance = largest_exchange_balance_dict_ordered[1][1]
    third_largest_exchange_balance = largest_exchange_balance_dict_ordered[2][1]
    fourth_largest_exchange_balance = largest_exchange_balance_dict_ordered[3][1]
    fifth_largest_exchange_balance = largest_exchange_balance_dict_ordered[4][1]
    top_five_dominance = largest_exchange_balance + second_largest_exchange_balance + third_largest_exchange_balance + fourth_largest_exchange_balance + fifth_largest_exchange_balance
    top_five_dominance = (top_five_dominance / total_balance)*100

    block_number_list.append(block_number)
    total_balance_list.append(weiToEth(total_balance))
    largest_exchange_balance_list.append(weiToEth(largest_exchange_balance))
    largest_exchange_name_list.append(largest_exchange_name)
    largest_exchange_dominance_list.append(largest_exchange_dominance)
    top_five_dominance_list.append(top_five_dominance)
    binance_list.append(weiToEth(binance))
    coinbase_list.append(weiToEth(coinbase))
    ftx_exchange_list.append(weiToEth(ftx_exchange))
    kraken_list.append(weiToEth(kraken))
    gate_io_list.append(weiToEth(gate_io))
    kucoin_list.append(weiToEth(kucoin))
    bitfinex_list.append(weiToEth(bitfinex))
    huobi_list.append(weiToEth(huobi))
    gemini_list.append(weiToEth(gemini))
    bitstamp_list.append(weiToEth(bitstamp))
    other_list.append(weiToEth(other))


    block_data = {
        'Block': block_number_list,
        'Total Balance': total_balance_list,
        'Largest Exchange Balance': largest_exchange_balance_list,
        'Largest Exchange Name': largest_exchange_name_list,
        'Largest Exchange Dominance': largest_exchange_dominance_list,
        'Top Five Dominance': top_five_dominance_list,
        'Binance': binance_list,
        'Coinbase': coinbase_list,
        'FTX Exchange': ftx_exchange_list,
        'Kraken': kraken_list,
        'Gate.io': gate_io_list,
        'KuCoin': kucoin_list,
        'Bitfinex': bitfinex_list,
        'Huobi': huobi_list,
        'Gemini': gemini_list,
        'Bitstamp': bitstamp_list,
        'Other': other_list

    }

    block_data_df = pd.DataFrame(block_data)
    block_data_df.to_csv('exchangeBalance.csv', mode='a', index=False, header=False)

    print(str(block) + ": " + str(total_balance))

# Remainder when dividing by 7200 is 5000
    
