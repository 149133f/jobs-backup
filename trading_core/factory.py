# -*- coding: utf-8 -*-
"""
Broker 工廠 - 統一建立券商實例
"""
from typing import Optional
from .interface import IBroker, MockBroker
from .config import Config


class BrokerFactory:
    """券商工廠"""
    
    _instances = {}  # 快取實例
    
    @classmethod
    def create(cls, broker_id: str = None, config: Config = None) -> IBroker:
        """
        建立券商實例
        Args:
            broker_id: 券商 ID (capital/unified/kitty/mock)
            config: 設定物件
        Returns:
            IBroker 實例
        """
        config = config or Config()
        broker_id = broker_id or config.active_broker
        
        # 如果已有實例，直接回傳
        if broker_id in cls._instances:
            return cls._instances[broker_id]
        
        # 建立新實例
        broker = cls._create_broker(broker_id, config)
        
        # 快取並回傳
        if broker:
            cls._instances[broker_id] = broker
        
        return broker
    
    @classmethod
    def _create_broker(cls, broker_id: str, config: Config) -> Optional[IBroker]:
        """建立券商"""
        
        # Mock (測試用)
        if broker_id == "mock":
            return MockBroker()
        
        # 群益期貨
        if broker_id == "capital":
            from .capital import CapitalBroker
            broker_config = config.get_broker_config("capital")
            if not broker_config:
                return None
            return CapitalBroker(
                account=broker_config.get("account", ""),
                password=broker_config.get("password", ""),
                dll_path=broker_config.get("dll_path", "")
            )
        
        # 統一期貨 (預留)
        if broker_id == "unified":
            # TODO: 實作統一期貨
            return None
        
        # 凱基期貨 (預留)
        if broker_id == "kitty":
            # TODO: 實作凱基期貨
            return None
        
        return None
    
    @classmethod
    def get_available_brokers(cls, config: Config = None) -> list:
        """取得可用的券商列表"""
        config = config or Config()
        available = []
        
        for broker_id, broker_config in config._config.get("brokers", {}).items():
            if broker_config.get("enabled", False):
                available.append({
                    "id": broker_id,
                    "name": broker_config.get("name", broker_id)
                })
        
        return available
    
    @classmethod
    def clear_cache(cls):
        """清除快取"""
        cls._instances = {}
