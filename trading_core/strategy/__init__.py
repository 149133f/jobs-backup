# -*- coding: utf-8 -*-
"""
Strategy Engine - 策略執行引擎
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Signal:
    """交易信號"""
    symbol: str
    side: str          # BUY/SELL
    price: float
    quantity: int
    reason: str
    timestamp: datetime


class IStrategy(ABC):
    """策略接口"""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @abstractmethod
    def on_tick(self, quote) -> Optional[Signal]:
        """報價更新時觸發"""
        pass
    
    @abstractmethod
    def on_bar(self, bar) -> Optional[Signal]:
        """K線收盤時觾發"""
        pass


class StrategyEngine:
    """策略引擎"""
    
    def __init__(self, broker, risk_engine):
        self.broker = broker
        self.risk_engine = risk_engine
        self.strategies: List[IStrategy] = []
        self.active_positions = {}
    
    def add_strategy(self, strategy: IStrategy):
        """新增策略"""
        self.strategies.append(strategy)
    
    def remove_strategy(self, name: str):
        """移除策略"""
        self.strategies = [s for s in self.strategies if s.name != name]
    
    def on_quote(self, symbol: str, quote):
        """報價更新"""
        for strategy in self.strategies:
            signal = strategy.on_tick(quote)
            if signal:
                # 經過風控檢查
                if self.risk_engine.check_signal(signal):
                    # 執行下單
                    self.execute_signal(signal)
    
    def on_bar(self, symbol: str, bar):
        """K線收盤"""
        for strategy in self.strategies:
            signal = strategy.on_bar(bar)
            if signal:
                if self.risk_engine.check_signal(signal):
                    self.execute_signal(signal)
    
    def execute_signal(self, signal: Signal):
        """執行信號"""
        # TODO: 呼叫 Order Router 下單
        pass
    
    def get_positions(self) -> Dict:
        """取得部位"""
        return self.active_positions


# 內建策略範例

class BreakoutStrategy(IStrategy):
    """突破策略"""
    
    def __init__(self):
        self.name = "突破策略"
        self.breakout_level = 0
        selfatrade = False
    
    @property
    def name(self) -> str:
        return self.name
    
    def on_bar(self, bar) -> Optional[Signal]:
        # 簡單突破邏輯
        if bar.high > self.breakout_level and not selfatrade:
            selfatrade = True
            return Signal(
                symbol=bar.symbol,
                side="BUY",
                price=bar.close,
                quantity=1,
                reason="突破",
                timestamp=datetime.now()
            )
        return None
    
    def on_tick(self, quote) -> Optional[Signal]:
        return None


class MeanReversionStrategy(IStrategy):
    """均值回歸策略"""
    
    def __init__(self):
        self.name = "均值回歸策略"
    
    @property
    def name(self) -> str:
        return self.name
    
    def on_bar(self, bar) -> Optional[Signal]:
        # 簡單均值回歸邏輯
        pass
    
    def on_tick(self, quote) -> Optional[Signal]:
        return None
