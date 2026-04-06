# -*- coding: utf-8 -*-
"""
Risk Engine - 風控系統
"""
from dataclasses import dataclass
from typing import Dict, Optional
from datetime import datetime


@dataclass
class RiskCheckResult:
    """風控檢查結果"""
    passed: bool
    message: str
    risk_level: str  # LOW/MEDIUM/HIGH


class RiskEngine:
    """風控引擎"""
    
    def __init__(self, config: Dict = None):
        # 風控參數
        self.max_position = config.get("max_position", 10)  # 最大部位
        self.max_loss_per_day = config.get("max_loss_per_day", 50000)  # 每日最大虧損
        self.max_order_size = config.get("max_order_size", 5)  # 單筆最大口數
        self.max_drawdown_pct = config.get("max_drawdown_pct", 10)  # 最大回撤%
        
        # 狀態
        self.today_pnl = 0  # 今日損益
        self.max_equity = 0  # 最高資產
        self.current_equity = 0  # 目前資產
    
    def check_signal(self, signal) -> RiskCheckResult:
        """
        檢查交易信號
        """
        # 檢查單筆口數
        if signal.quantity > self.max_order_size:
            return RiskCheckResult(
                passed=False,
                message=f"單筆口數超過限制 {self.max_order_size}",
                risk_level="HIGH"
            )
        
        # 檢查部位數
        current_position = self.get_total_position()
        if current_position + signal.quantity > self.max_position:
            return RiskCheckResult(
                passed=False,
                message=f"部位超過限制 {self.max_position}",
                risk_level="HIGH"
            )
        
        # 檢查今日虧損
        if self.today_pnl < -self.max_loss_per_day:
            return RiskCheckResult(
                passed=False,
                message=f"今日虧損達到限制 {self.max_loss_per_day}",
                risk_level="HIGH"
            )
        
        # 檢查回撤
        if self.current_equity > 0:
            drawdown = (self.max_equity - self.current_equity) / self.max_equity * 100
            if drawdown > self.max_drawdown_pct:
                return RiskCheckResult(
                    passed=False,
                    message=f"回撤超過限制 {self.max_drawdown_pct}%",
                    risk_level="HIGH"
                )
        
        return RiskCheckResult(
            passed=True,
            message="通過風控檢查",
            risk_level="LOW"
        )
    
    def check_order(self, order) -> RiskCheckResult:
        """檢查委託"""
        return self.check_signal(order)
    
    def update_pnl(self, pnl: float):
        """更新損益"""
        self.today_pnl += pnl
    
    def update_equity(self, equity: float):
        """更新資產"""
        self.current_equity = equity
        if equity > self.max_equity:
            self.max_equity = equity
    
    def get_total_position(self) -> int:
        """取得總部位"""
        # TODO: 從 取得
        broker return 0
    
    def reset_daily(self):
        """每日重置"""
        self.today_pnl = 0
    
    def get_status(self) -> Dict:
        """取得風控狀態"""
        return {
            "today_pnl": self.today_pnl,
            "max_position": self.max_position,
            "current_position": self.get_total_position(),
            "max_loss_per_day": self.max_loss_per_day,
            "max_drawdown_pct": self.max_drawdown_pct,
            "current_equity": self.current_equity,
            "max_equity": self.max_equity
        }
