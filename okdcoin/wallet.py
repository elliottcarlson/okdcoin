# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
from okdcoin.block import Block
from sqlalchemy import or_, func


class Wallet(object):
    ledger = {}

    def __init__(self, session, owner):
        self.session = session
        self.owner = owner
        self.balance = self.get_balance()

    def get_balance(self):
        if self.owner not in Wallet.ledger:
            balance = 0
            q = '%%"%s"%%' % self.owner
            blocks = self.session.query(
                func.json_extract(Block.data, '$.transactions[*].to'),
                func.json_extract(Block.data, '$.transactions[*].from'),
                func.json_extract(Block.data, '$.transactions[*].amount'),
            ).filter(or_(
                func.json_extract(Block.data, '$.transactions[*].to').like(q),
                func.json_extract(Block.data, '$.transactions[*].from').like(q)
            )).all()

            for block in blocks:
                _t, _f, _a = block
                _t = json.loads(_t)
                _f = json.loads(_f)
                _a = json.loads(_a)
                data = [{'t': t, 'f': f, 'a': a} for t, f, a in zip(_t, _f, _a)]

                for transaction in data:
                    if transaction['f'] == self.owner:
                        balance -= transaction['a']
                    elif transaction['t'] == self.owner:
                        balance += transaction['a']

            Wallet.ledger[self.owner] = balance

        return Wallet.ledger[self.owner]

    def update_balance(self):
        if self.owner in Wallet.ledger:
            del Wallet.ledger[self.owner]

        return self.get_balance()
