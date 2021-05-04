from web3 import Web3

def sendTransaction(message):
    w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/1c67da5e24c94a25979254615f5c4b09'))
    address = '0xc6e6D183Da2E8fa6e18511b6e438fb7D75cEd523'
    privateKey = '0x21b3e754a5d041a79ccaa4cb77b0e65bf14d30f5b535ea142afcc98a71bb7460'
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    value = w3.toWei(0, 'ether')
    signedTx = w3.eth.account.signTransaction(dict(
        nonce=nonce,
        gasPrice=gasPrice,
        gas= 1000000,
        to='0x0000000000000000000000000000000000000000',
        value=value,
        data=message.encode('utf-8')
    ), privateKey)

    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    return txId