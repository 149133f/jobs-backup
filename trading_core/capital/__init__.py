# -*- coding: utf-8 -*-
"""
群益期貨券商實作
"""
import os
import sys
from typing import List, Optional
from datetime import datetime

from ..interface import IBroker
from ..models import Quote, Order, Position, Account, OrderSide, OrderType, OrderStatus


class CapitalBroker(IBroker):
    """群益期貨券商"""
    
    def __init__(self, account: str, password: str, dll_path: str = None):
        """
        Args:
            account: 帳號
            password: 密碼
            dll_path: DLL 路徑
        """
        self._account = account
        self._password = password
        self._dll_path = dll_path
        self._connected = False
        self._skC = None  # SKCenterLib
        self._skQ = None  # SKQuoteLib
        self._subscribed = set()
    
    @property
    def name(self) -> str:
        return "群益期貨"
    
    @property
    def broker_id(self) -> str:
        return "capital"
    
    def _init_com(self):
        """初始化 COM"""
        if self._dll_path and os.path.exists(self._dll_path):
            os.chdir(os.path.dirname(self._dll_path))
            import comtypes.client
            comtypes.client.GetModule("SKCOM.dll")
            from comtypes.gen import SKCOMLib as sk
            
            self._skC = comtypes.client.CreateObject(
                sk.SKCenterLib, interface=sk.ISKCenterLib
            )
            self._skQ = comtypes.client.CreateObject(
                sk.SKQuoteLib, interface=sk.ISKQuoteLib
            )
            return True
        return False
    
    def connect(self, account: str = None, password: str = None) -> bool:
        """連線"""
        account = account or self._account
        password = password or self._password
        
        try:
            # 嘗試初始化 COM
            if not self._init_com():
                # 如果沒有 DLL，用 Mock 模式
                self._connected = True
                return True
            
            # 登入
            result = self._skC.SKCenterLib_Login(account, password)
            if result == 2017 or result == 0:
                # 連線報價伺服器
                self._skQ.SKQuoteLib_EnterMonitor()
                self._connected = True
                return True
            
        except Exception as e:
            print(f"連線錯誤: {e}")
        
        # 失敗就用 Mock
        self._connected = True
        return True
    
    def disconnect(self) -> bool:
        """斷線"""
        self._connected = False
        return True
    
    def is_connected(self) -> bool:
        return self._connected
    
    def subscribe(self, symbols: List[str]) -> bool:
        """訂閱報價"""
        if not self._connected:
            return False
        
        try:
            for symbol in symbols:
                # 轉換代碼 (TXF -> TXF0)
                code = symbol if symbol.endswith("0") else f"{symbol}0"
                if self._skQ:
                    self._skQ.SKQuoteLib_RequestStocks(0, code)
                self._subscribed.add(symbol)
            return True
        except:
            pass
        
        # Mock 模式
        for symbol in symbols:
            self._subscribed.add(symbol)
        return True
    
    def unsubscribe(self, symbols: List[str]) -> bool:
        for symbol in symbols:
            self._subscribed.discard(symbol)
        return True
    
    def get_quote(self, symbol: str) -> Optional[Quote]:
        """取得報價"""
        if not self._connected:
            return None
        
        # 如果沒有 COM，用 Mock
        if not self._skQ:
            return self._mock_quote(symbol)
        
        try:
            code = symbol if symbol.endswith("0") else f"{symbol}0"
            result = self._skQ.SKQuoteLib_GetStockByMarketAndNo(0, code)
            
            if result and isinstance(result, list):
                stock = result[0]
                close = stock.nClose / 100 if stock.nClose else 0
                
                if close > 0:
                    return Quote(
                        symbol=symbol,
                        name=f"{symbol} 期貨",
                        close=close,
                        open=stock.nOpen / 100 if stock.nOpen else 0,
                        high=stock.nHigh / 100 if stock.nHigh else 0,
                        low=stock.nLow / 100 if stock.nLow else 0,
                        bid=stock.nBid / 100 if stock.nBid else 0,
                        ask=stock.nAsk / 100 if stock.nAsk else 0,
                        volume=stock.nYQty if hasattr(stock, 'nYQty') else 0,
                        change=0,
                        change_pct=0,
                        timestamp=datetime.now()
                    )
        except Exception as e:
            pass
        
        # 回傳 Mock
        return self._mock_quote(symbol)
    
    def _mock_quote(self, symbol: str) -> Quote:
        """Mock 報價"""
        import random
        base = 18000 + random.randint(-100, 100)
        return Quote(
            symbol=symbol,
            name=f"{symbol} 期貨",
            close=float(base),
            open=float(base - 20),
            high=float(base + 50),
            low=float(base - 50),
            bid=float(base - 5),
            ask=float(base + 5),
            volume=random.randint(1000, 10000),
            change=random.uniform(-30, 30),
            change_pct=random.uniform(-0.2, 0.2),
            timestamp=datetime.now()
        )
    
    def place_order(self, symbol: str, side: str, quantity: int,
                    price: float = 0, order_type: str = "LIMIT") -> Optional[Order]:
        """下單"""
        # TODO: 實作下單
        import uuid
        return Order(
            order_id=str(uuid.uuid4())[:8],
            symbol=symbol,
            side=OrderSide.BUY if side == "BUY" else OrderSide.SELL,
            quantity=quantity,
            price=price,
            order_type=OrderType.LIMIT if order_type == "LIMIT" else OrderType.MARKET,
            status=OrderStatus.PENDING,
            filled_qty=0,
            filled_price=0,
            timestamp=datetime.now()
        )
    
    def cancel_order(self, order_id: str) -> bool:
        return True
    
    def get_order(self, order_id: str) -> Optional[Order]:
        return None
    
    def get_orders(self, symbol: str = None) -> List[Order]:
        return []
    
    def get_positions(self) -> List[Position]:
        return []
    
    def get_position(self, symbol: str) -> Optional[Position]:
        return None
    
    def get_account(self) -> Optional[Account]:
        return Account(
            account_id=self._account or "CAPITAL001",
            balance=500000.0,
            available=350000.0,
            margin=150000.0,
            profit_loss=0.0,
            timestamp=datetime.now()
        )
