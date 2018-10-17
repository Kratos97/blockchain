from hashlib import sha256
import json
import time

class Block:


    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.transactions = transactions
        #self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0

    def compute_hash(self):
        """
        A function that return the hash of the block contents.
        """
        #block_string = self.transactions+str(self.nonce)
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()

    def proof_of_work(self, block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * 5):
            block.nonce += 1
            computed_hash = block.compute_hash()
            print(computed_hash)
        print('最终结果是:{}, 随机数:{}'.format(computed_hash,block.nonce))

        return computed_hash