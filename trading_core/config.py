# -*- coding: utf-8 -*-
"""
設定檔 - 券商配置
"""
import json
import os
from typing import Optional


class Config:
    """交易系統配置"""
    
    DEFAULT_CONFIG_PATH = "~/.openclaw/trading_config.json"
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.expanduser(self.DEFAULT_CONFIG_PATH)
        self._config = self._load()
    
    def _load(self) -> dict:
        """載入配置"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        return self._default()
    
    def _default(self) -> dict:
        """預設配置"""
        return {
            "version": "1.0",
            "active_broker": "capital",  # 目前使用的券商
            "brokers": {
                "capital": {
                    "name": "群益期貨",
                    "enabled": True,
                    "account": "",
                    "password": "",
                    "dll_path": "C:/Users/Feng/Downloads/CapitalAPI_2.13.57_PythonExample/元件/x86/SKCOM.dll"
                },
                "unified": {
                    "name": "統一期貨",
                    "enabled": False,
                    "account": "",
                    "password": "",
                    "api_url": ""
                },
                "kitty": {
                    "name": "凱基期貨",
                    "enabled": False,
                    "account": "",
                    "password": "",
                    "api_url": ""
                }
            },
            "symbols": {
                "TXF": "台指期",
                "MTX": "小台指",
                "TE": "電指期",
                "TF": "金融期"
            },
            "risk": {
                "max_position": 10,
                "max_loss_per_day": 50000,
                "max_order_size": 5
            }
        }
    
    def save(self):
        """儲存配置"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, ensure_ascii=False, indent=2)
    
    @property
    def active_broker(self) -> str:
        """取得目前券商"""
        return self._config.get("active_broker", "capital")
    
    @active_broker.setter
    def active_broker(self, broker_id: str):
        """設定目前券商"""
        self._config["active_broker"] = broker_id
        self.save()
    
    def get_broker_config(self, broker_id: str) -> Optional[dict]:
        """取得券商配置"""
        return self._config.get("brokers", {}).get(broker_id)
    
    def is_broker_enabled(self, broker_id: str) -> bool:
        """券商是否啟用"""
        config = self.get_broker_config(broker_id)
        return config.get("enabled", False) if config else False
    
    def enable_broker(self, broker_id: str):
        """啟用券商"""
        if broker_id in self._config["brokers"]:
            self._config["brokers"][broker_id]["enabled"] = True
            self.save()
    
    def disable_broker(self, broker_id: str):
        """停用券商"""
        if broker_id in self._config["brokers"]:
            self._config["brokers"][broker_id]["enabled"] = False
            self.save()
    
    def set_broker_credentials(self, broker_id: str, account: str, password: str):
        """設定券商帳號密碼"""
        if broker_id in self._config["brokers"]:
            self._config["brokers"][broker_id]["account"] = account
            self._config["brokers"][broker_id]["password"] = password
            self.save()


# 全域配置實例
config = Config()
