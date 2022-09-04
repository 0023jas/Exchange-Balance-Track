from web3 import Web3
import requests


#w3 = Put you ipc, http, or rpc provider in here! 

# Gets the current state of the node
currentState = w3.eth.syncing

# Block to be analyzed
block = 15068001

# Gets the latest block number
latestBlock = w3.eth.getBlock('latest')
latestBlockNumber = latestBlock.number

# Current block reward
block_reward = 2

# Gets details of a given block 
def blockDetails(blockNumber):
    return w3.eth.get_block(blockNumber)

def transactionDetails(txHash):
    return w3.eth.get_transaction(txHash)

# Gets transaction count of a given block
def transactionCount(givenBlock):
    return len(givenBlock['transactions'])

# Converts wei value to eth value
def weiToEth(wei):
    eth = wei / 1000000000000000000
    return eth

def weiToGwei(wei):
    gwei = wei / 1000000000
    return gwei

def getEthTotalSupply():
    response = requests.get('https://api.etherscan.io/api?module=stats&action=ethsupply&apikey=Z3586PZ736ZBX3KXSYK81QD2Z284QW5W9Q').json()
    ethTotalSupply = response['result']
    return weiToEth(int(ethTotalSupply))

# Gets the basic details of a block
def getBlockInfo(givenBlock):
    blockDifficulty = givenBlock['difficulty']
    blockTransactionCount = len(givenBlock['transactions'])
    blockNumber = givenBlock['number']
    blockSize = givenBlock['size']
    blockTimestamp = givenBlock['timestamp']
    blockTotalDifficulty = givenBlock['totalDifficulty']
    return blockDifficulty, blockTransactionCount, blockNumber, blockSize, blockTimestamp, blockTotalDifficulty

# Calculates the burnt fees of a given block
def calcFeesBurnt(givenBlock):
    if(givenBlock['number'] >= 12965000):
        baseFee = int(givenBlock['baseFeePerGas'])
        gasUsed = givenBlock['gasUsed']
        gasLimit = givenBlock['gasLimit']
        totalBurnt = gasUsed * baseFee
        return weiToGwei(baseFee), gasUsed, gasLimit, weiToEth(totalBurnt)
    else:
        return 0

# Calculate Tx Cost
def calcTxCost(transaction):
    #Prior to the London Upgrade
    if(transaction['blockNumber'] < 12965000):
        gasUsed = transaction['gas']
        gasPrice = transaction['gasPrice']
        txCost = gasUsed * gasPrice
    # After the London Upgrade
    elif(transaction['blockNumber'] >= 12965000):
        gasUsed = transaction['gas']
        gasPrice = transaction['gasPrice']
        txCost = gasUsed * gasPrice
    
    return weiToEth(txCost)

def getAddressBalanceAtBlock(address, block):
    return w3.eth.getBalance(address, block)

# Uncles and uncle rewards
def getUncleCount(block):
    uncle_list = w3.eth.getBlock(block).uncles
    return len(uncle_list)

def getUncleDetails(uncle_count, block):
    uncle_details = []

    for uncle in range(0, uncle_count):
        uncle_details.append(w3.eth.get_uncle_by_block(block, uncle))

    return uncle_details

def getBlockUncleReward(uncle_list, block):
    # Uncle reward starts at block reward
    # Uncle reward depreciates at 1/8th per block between uncle and mined block
    # Uncle reward is 0 if distance between uncle and mined block is greater than 6
    uncle_reward = 0
    for uncle in range(len(uncle_list)):
        uncle_number = uncle_list[uncle]['number']
        uncle_number = int(uncle_number, 16)
        uncle_distance = block - uncle_number
        if(uncle_distance <= 6):
            uncle_reward += block_reward * ((8 - uncle_distance) / 8)

    return uncle_reward

"""
txReceipt = w3.eth.get_transaction_receipt(blockDetails(14901189)['transactions'][1])
txCumulativeGas = txReceipt['effectiveGasPrice']
print(txCumulativeGas)
print(blockDetails(14901189)['baseFeePerGas'])
"""



#print(blockDetails(12966000))
#print(transactionDetails('0x1d17ae0d177dcfc51a15c0281eae3df151850af4485d5d3cfaf1889f90e405c8'))
#print(calcTxCost(transactionDetails('0xb189aee527c06c6d784ab71356e1023cda7899ce89697ff58c22c82bff90b551')))
#print(21000*70578812137)
#print(calcTxCost(transactionDetails('0xf53d7a6f3cfe4189cdcf536b5766ffd803364f24bdb18dd8088e6ddd30cdf33d')))
#print(blockDetails(100))
#print(i3.eth.get_balance('0xbb7B8287f3F0a933474a79eAe42CBCa977791171', 100))
#print(i3.eth.estimate_gas({'to': '0xd3CdA913deB6f67967B99D67aCDFa1712C293601', 'from':'0x4A5EfA846e7375a40DcD596c7C6DAdB28df28AE4', 'value': 12345}, 12965000))
#print(getEthTotalSupply())
#print(i3.eth.max_priority_fee)
#print(latestBlockNumber)





#print(latestBlockNumber, transactionCount, ethTotalBurn)
"""
totalTransactions = 0
count = 0
ethTotalBurnt = 0
for i in range(12964000, latestBlockNumber):
    block = w3.eth.get_block(i)
    totalTransactions += len(block['transactions'])

    if(i >= 12965000):
        baseFee = int(block['baseFeePerGas'])
        gasUsed = block['gasUsed']
        Burnt = gasUsed * baseFee
        ethBurnt = w3.fromWei(Burnt, 'ether')
        ethTotalBurnt += ethBurnt
        

    count += 1

    if(count == 1000):
        print(i, totalTransactions, ethTotalBurnt)
        count = 0


print(totalTransactions, i)
"""