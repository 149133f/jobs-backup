# -*- coding: utf-8 -*-
"""
Broker 接口定義 - 所有券商必須實作的接口
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Quote, Order, Position, Account


class IBroker(ABC):
    """券商接口 - 定義統一的功能"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """券商名稱"""
        pass
    
    @property
    @abstractmethod
    def broker_id(self) -> str:
        """券商 ID"""
        pass
    
    # ========== 連線 ==========
    
    @abstractmethod
    def connect(self, account: str, password: str) -> bool:
        """
        連線/登入
        Returns: 是否成功
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """
        斷線
        Returns: 是否成功
        """
        pass
    
    @abstractmethod
    def is_connected(self) -> bool:
        """
        檢查是否連線
        """
        pass
    
    # ========== 報價 ==========
    
    @abstractmethod
    def subscribe(self, symbols: List[str]) -> bool:
        """
        訂閱報價
        Args:
            symbols: 商品代碼列表，如 ['TXF', 'MTX']
        Returns: 是否成功
        """
        pass
    
    @abstractmethod
    def unsubscribe(self, symbols: List[str]) -> bool:
        """
        取消訂閱
        """
        pass
    
    @abstractmethod
    def get_quote(self, symbol: str) -> Optional[Quote]:
        """
        取得報價
        Args:
            symbol: 商品代碼
        Returns:
            Quote 物件，失敗回傳 None
        """
        pass
    
    # ========== 委託 ==========
    
    @abstractmethod
    def place_order(self, symbol: str, side: str, quantity: int, 
                    price: float = 0, order_type: str = "LIMIT") -> Optional[Order]:
        """
        下單
        Args:
            symbol: 商品代碼
            side: 'BUY' 或 'SELL'
            quantity: 數量
            price: 價格 (市價填 0)
            order_type: 'MARKET' 或 'LIMIT'
        Returns:
            Order 物件，失敗回傳 None
        """
        pass
    
    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """
        取消委託
        Args:
            order_id: 委託編號
        Returns: 是否成功
        """
        pass
    
    @abstractmethod
    def get_order(self, order_id: str) -> Optional[Order]:
        """
        查詢委託
        """
        pass
    
    @abstractmethod
    def get_orders(self, symbol: Optional[str] = None) -> List[Order]:
        """
        取得所有委託
        """
        pass
    
    # ========== 部位 ==========
    
    @abstractmethod
    def get_positions(self) -> List[Position]:
        """
        取得所有部位
        """
        pass
    
    @abstractmethod
    def get_position(self, symbol: str) -> Optional[Position]:
        """
        取得特定商品部位
        """
        pass
    
    # ========== 帳戶 ==========
    
    @abstractmethod
    def get_account(self) -> Optional[Account]:
        """
        取得帳戶資訊
        """
        pass


class MockBroker(IBroker):
    """Mock 券商 - 用於測試"""
    
    def __init__(self):
        self._connected = False
        self._account = None
    
    @property
    def name(self) -> str:
        return "Mock Broker"
    
    @property
    def broker_id(self) -> str:
        return "MOCK"
    
    def connect(self, account: str, password: str) -> bool:
        self._connected = True
        self._account = account
        return True
    
    def disconnect(self) -> bool:
        self._connected = False
        return True
    
    def is_connected(self) -> bool:
        return self._connected
    
    def subscribe(self, symbols: List[str]) -> bool:
        return True
    
    def unsubscribe(self, symbols: List[str]) -> bool:
        return True
    
    def get_quote(self, symbol: str) -> Optional[Quote]:
        from datetime import datetime
        return Quote(
            symbol=symbol,
            name=f"{symbol} 期貨",
            close=18000.0,
            open=17950.0,
            high=18100.0,
            low=17900.0,
            bid=17995.0,
            ask=18005.0,
            volume=5000,
            change=50.0,
            change_pct=0.28,
            timestamp=datetime.now()
        )
    
    def place_order(self, symbol: str, side: str, quantity: int,
                    price: float = 0, order_type: str = "LIMIT") -> Optional[Order]:
        from datetime import datetime
        import uuid
        return Order(
            order_id=str(uuid.uuid4())[:8],
            symbol=symbol,
            side=side,
            quantity=quantity,
            price=price,
            order_type=order_type,
            status="FILLED",
            filled_qty=quantity,
            filled_price=price or 18000.0,
            timestamp=datetime.now()
        )
    
    def cancel_order(self, order_id: str) -> bool:
        return True
    
    def get_order(self, order_id: str) -> Optional[Order]:
        return None
    
    def get_orders(self, symbol: Optional[str] = None) -> List[Order]:
        return []
    
    def get_positions(self) -> List[Position]:
        return []
    
    def get_position(self, symbol: str) -> Optional[Position]:
        return None
    
    def get_account(self) -> Optional[Account]:
        from datetime import datetime
        return Account(
            account_id="MOCK001",
            balance=500000.0,
            available=350000.0,
            margin=150000.0,
            profit_loss=0.0,
            timestamp=datetime.now()
        )
