#!/usr/bin/env python
from __future__ import absolute_import
from okdcoin.exceptions import InsufficientFunds
from okdcoin.okdcoin import OKDCoin
from random import choice, uniform


names = [
    'digx',
    'jbz',
    'lostcuaz',
    'sublimnl',
    'erikbeta',
    'jcb',
    'realvinay',
    'woxidu',
    'Euj',
    'jsbronder',
    'melanarchy',
    'sherman',
    'jgarf',
    'bgarf',
    'MongoBot'
]

msgs = [
    'weed money',
    'funny joke',
    'good butt play',
    'thanks for drinks',
    'don\'t need a damn reason',
    None
]


def main():
    okd = OKDCoin()

    for i in range(1, 1000):
        if choice([0, 1]):
            user = choice(names)
            balance = okd.get_balance(user)
            print('%s had a balance of %s OKD' % (user, balance))
            okd.mine_block(user)
            print('%s mined a new block and earned 25 OKD' % user)
            balance = okd.get_balance(user)
            print('%s now has a balance of %s OKD' % (user, balance))
        else:
            sender = choice(names)
            receiver = choice([x for i, x in enumerate(names) if i != sender])
            msg = choice(msgs)
            amount = uniform(1, 20)
            balance = okd.get_balance(sender)
            print('%s had a balance of %s OKD' % (sender, balance))
            balance = okd.get_balance(receiver)
            print('%s had a balance of %s OKD' % (receiver, balance))
            print('%s is trying to send %s %sOKD; message was: %s' % (
                sender, receiver, amount, msg
            ))
            try:
                okd.new_transaction(sender, receiver, amount, msg)
            except InsufficientFunds:
                print('It failed due to insufficient funds!')
            balance = okd.get_balance(sender)
            print('%s now has a balance of %s OKD' % (sender, balance))
            balance = okd.get_balance(receiver)
            print('%s now has a balance of %s OKD' % (receiver, balance))

        print('=' * 40)


if __name__ == '__main__':
    main()
