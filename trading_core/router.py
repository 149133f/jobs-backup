# -*- coding: utf-8 -*-
"""
Order Router - 委託路由器
"""
from typing import List, Optional
from .models import Order, Quote
from .interface import IBroker


class OrderRouter:
    """委託路由器 - 支援多券商"""
    
    def __init__(self, brokers: dict = None):
        """
        Args:
            brokers: {broker_id: IBroker實例}
        """
        self._brokers = brokers or {}
        self._primary_broker = None
    
    def add_broker(self, broker_id: str, broker: IBroker, is_primary: bool = False):
        """新增券商"""
        self._brokers[broker_id] = broker
        if is_primary:
            self._primary_broker = broker_id
    
    def remove_broker(self, broker_id: str):
        """移除券商"""
        if broker_id in self._brokers:
            del self._brokers[broker_id]
        if self._primary_broker == broker_id:
            self._primary_broker = None
    
    @property
    def primary_broker(self) -> Optional[str]:
        return self._primary_broker
    
    def set_primary(self, broker_id: str):
        """設定主要券商"""
        if broker_id in self._brokers:
            self._primary_broker = broker_id
    
    def get_broker(self, broker_id: str = None) -> Optional[IBroker]:
        """取得券商"""
        broker_id = broker_id or self._primary_broker
        return self._brokers.get(broker_id)
    
    def get_quote(self, symbol: str, broker_id: str = None) -> Optional[Quote]:
        """取得報價"""
        broker = self.get_broker(broker_id)
        if broker:
            return broker.get_quote(symbol)
        return None
    
    def get_quotes(self, symbol: str) -> dict:
        """從所有券商取得報價"""
        quotes = {}
        for bid, broker in self._brokers.items():
            quote = broker.get_quote(symbol)
            if quote:
                quotes[bid] = quote
        return quotes
    
    def place_order(self, symbol: str, side: str, quantity: int,
                   price: float = 0, order_type: str = "LIMIT",
                   broker_id: str = None) -> Optional[Order]:
        """下單"""
        broker = self.get_broker(broker_id)
        if broker:
            return broker.place_order(symbol, side, quantity, price, order_type)
        return None
    
    def get_all_positions(self) -> dict:
        """取得所有券商部位"""
        positions = {}
        for broker_id, broker in self._brokers.items():
            pos = broker.get_positions()
            if pos:
                positions[broker_id] = pos
        return positions
    
    def get_all_accounts(self) -> dict:
        """取得所有券商帳戶"""
        accounts = {}
        for broker_id, broker in self._brokers.items():
            acc = broker.get_account()
            if acc:
                accounts[broker_id] = acc
        return accounts
