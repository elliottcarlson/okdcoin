# -*- coding: utf-8 -*-
from __future__ import absolute_import
import hashlib

from okdcoin.db import Base
from sqlalchemy import Column, Integer, JSON, String, TIMESTAMP


class Block(Base):
    __tablename__ = 'block'

    id = Column(Integer, nullable=True, primary_key=True)
    ts = Column(TIMESTAMP)
    data = Column(JSON)
    prev_hash = Column(String(64))
    hash = Column(String(64))

    def __init__(self, index, ts, data, prev_hash):
        self.id = index
        self.ts = ts
        self.data = data
        self.prev_hash = prev_hash
        self.hash = self.hash_block()

    def hash_block(self):
        sha = hashlib.sha256()
        sha.update(
            str(self.id) +
            str(self.ts) +
            str(self.data) +
            str(self.prev_hash)
        )
        return sha.hexdigest()

    def __str__(self):
        return (
            '<Block(index={0}, ts={1}, data={2}, prev_hash={3})> = {4}'
        ).format(self.id, self.ts, self.data, self.prev_hash, self.hash)

    def __repr__(self):
        return self.__str__()
