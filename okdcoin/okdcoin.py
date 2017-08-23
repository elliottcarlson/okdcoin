# -*- coding: utf-8 -*-
from __future__ import absolute_import
from datetime import datetime
from okdcoin.block import Block
from okdcoin.db import Base, engine
from okdcoin.exceptions import InsufficientFunds, UnableToMineNewBlock
from okdcoin.wallet import Wallet
from sqlalchemy.orm import Session


class OKDCoin(object):
    pending_transactions = []

    def __init__(self):
        Base.metadata.create_all(engine)
        self.session = Session(bind=engine)
        self.session.commit()

    def _create_genesis_block(self):
        self.new_transaction('network', 'MongoBot', 10000, 'Genesis pre-mine')
        try:
            block = Block(
                1,
                datetime.now(),
                {
                    'transactions': OKDCoin.pending_transactions,
                },
                '0',
            )
            self.session.add(block)
            self.session.commit()

            OKDCoin.pending_transactions = []

            return block
        except:
            self.session.rollback()
            raise UnableToMineNewBlock('Genesis block fail.')

        return 'Genesis block already generated.'

    def test_balance(self, user):
        return Wallet(self.session, user).test_balance()

    def has_balance(self, user, amount=0):
        balance = self.get_balance(user)
        if balance:
            return True if balance > amount else False

    def get_balance(self, user):
        return Wallet(self.session, user).get_balance()

    def new_transaction(self, sender, receiver, amount, comment=None):
        if sender is not 'network' and not self.has_balance(sender, amount):
            raise InsufficientFunds()

        print('New transaction (%s, %s, %s)' % (sender, receiver, amount))
        OKDCoin.pending_transactions.append(
            {
                'from': sender,
                'to': receiver,
                'amount': amount,
                'comment': comment
            }
        )

    def last_block(self):
        last_block = self.session.query(Block).order_by(Block.id.desc()).first()

        if not last_block:
            last_block = self._create_genesis_block()

        return last_block

    def mine_block(self, miner='MongoBot'):
        last_block = self.last_block()

        self.new_transaction('network', miner, 25, 'Mining reward.')

        block = Block(
            int(last_block.id) + 1,
            datetime.now(),
            {
                'transactions': OKDCoin.pending_transactions
            },
            last_block.hash
        )

        try:
            self.session.add(block)
            self.session.commit()

            data = OKDCoin.pending_transactions
            users = set([d['from'] for d in data] + [d['to'] for d in data])
            users.discard('network')
            print('Resolving pending transactions for: %s' % users)
            print(OKDCoin.pending_transactions)
            for user in users:
                balance = self.get_balance(user)
                print('%s has %s OKD' % (user, balance))
                print('Updating balance...')
                Wallet(self.session, user).update_balance()
                balance = self.get_balance(user)
                print('%s now has %s OKD' % (user, balance))

            OKDCoin.pending_transactions = []

            return block
        except Exception as e:
            self.session.rollback()
            raise UnableToMineNewBlock(str(e))
