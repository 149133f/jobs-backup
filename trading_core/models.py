# -*- coding: utf-8 -*-
"""
資料模型 - 統一資料格式
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class OrderSide(Enum):
    """買賣方向"""
    BUY = "BUY"
    SELL = "SELL"


class OrderType(Enum):
    """委託類型"""
    MARKET = "MARKET"      # 市價
    LIMIT = "LIMIT"       # 限價


class OrderStatus(Enum):
    """委託狀態"""
    PENDING = "PENDING"       # 等待中
    FILLED = "FILLED"         # 已成交
    CANCELLED = "CANCELLED"   # 已取消
    REJECTED = "REJECTED"     # 已拒絕


@dataclass
class Quote:
    """報價"""
    symbol: str              # 商品代碼 (如 TXF)
    name: str                # 商品名稱
    close: float              # 成交價
    open: float              # 開盤價
    high: float              # 最高價
    low: float               # 最低價
    bid: float               # 買價
    ask: float               # 賣價
    volume: int              # 成交量
    change: float            # 漲跌
    change_pct: float        # 漲跌幅%
    timestamp: datetime       # 時間
    
    def to_dict(self):
        return {
            "symbol": self.symbol,
            "name": self.name,
            "close": self.close,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "bid": self.bid,
            "ask": self.ask,
            "volume": self.volume,
            "change": self.change,
            "change_pct": self.change_pct,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class Order:
    """委託單"""
    order_id: str            # 委託編號
    symbol: str              # 商品代碼
    side: OrderSide          # 買/賣
    quantity: int           # 數量
    price: float            # 價格
    order_type: OrderType    # 市價/限價
    status: OrderStatus      # 狀態
    filled_qty: int         # 已成交數量
    filled_price: float      # 成交價格
    timestamp: datetime      # 時間
    
    def to_dict(self):
        return {
            "order_id": self.order_id,
            "symbol": self.symbol,
            "side": self.side.value,
            "quantity": self.quantity,
            "price": self.price,
            "order_type": self.order_type.value,
            "status": self.status.value,
            "filled_qty": self.filled_qty,
            "filled_price": self.filled_price,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class Position:
    """部位"""
    symbol: str              # 商品代碼
    quantity: int           # 數量 (+多/-空)
    avg_price: float         # 平均價格
    current_price: float    # 現在價格
    profit_loss: float      # 損益
    margin: float           # 保證金
    timestamp: datetime     # 時間
    
    def to_dict(self):
        return {
            "symbol": self.symbol,
            "quantity": self.quantity,
            "avg_price": self.avg_price,
            "current_price": self.current_price,
            "profit_loss": self.profit_loss,
            "margin": self.margin,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class Account:
    """帳戶"""
    account_id: str         # 帳號
    balance: float          # 帳戶餘額
    available: float        # 可用金額
    margin: float          # 佔用保證金
    profit_loss: float      # 總損益
    timestamp: datetime     # 時間
    
    def to_dict(self):
        return {
            "account_id": self.account_id,
            "balance": self.balance,
            "available": self.available,
            "margin": self.margin,
            "profit_loss": self.profit_loss,
            "timestamp": self.timestamp.isoformat()
        }
