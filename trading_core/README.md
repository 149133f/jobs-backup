# Trading Core - 交易系統核心
# 基礎架構 v1.0

## 目錄結構

```
trading_core/
├── __init__.py
├── config.py           # 設定檔
├── models.py           # 資料模型
├── interface.py        # Broker 接口定義
├── factory.py          # Broker 工廠
├── router.py          # 委託路由器
├── capital/           # 群益券商實作
│   ├── __init__.py
│   └── capital_broker.py
├── unified/           # 統一券商實作（預留）
├── kitty/             # 凱基券商實作（預留）
└── tests/             # 測試
```

## 設計原則

1. **統一路由** - 所有券商透過同一接口
2. **可插拔** - 新增券商只需實作接口
3. **配置優先** - 切換券商只需改設定

## 使用方式

```python
from trading_core import BrokerFactory, Config

# 從設定建立 Broker
broker = BrokerFactory.create('capital')

# 取得報價
quote = broker.get_quote('TXF')

# 下單
order = broker.place_order('TXF', 'BUY', 1, 18500)
```
