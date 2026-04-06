# -*- coding: utf-8 -*-
"""
測試 Trading Core
"""

# 測試1: 使用 Mock Broker
print("=" * 50)
print("測試1: Mock Broker")
print("=" * 50)

from trading_core import BrokerFactory, Config

# 建立 Mock Broker
broker = BrokerFactory.create("mock")

# 連線
print(f"連線: {broker.connect('test', 'test')}")
print(f"券商: {broker.name}")

# 取得報價
quote = broker.get_quote("TXF")
print(f"\n報價:")
print(f"  商品: {quote.symbol}")
print(f"  價格: {quote.close}")
print(f"  漲跌: {quote.change:.2f} ({quote.change_pct:.2f}%)")

# 取得帳戶
account = broker.get_account()
print(f"\n帳戶:")
print(f"  帳號: {account.account_id}")
print(f"  餘額: {account.balance:,.0f}")
print(f"  可用: {account.available:,.0f}")

print("\n" + "=" * 50)
print("測試2: Capital Broker (Mock 模式)")
print("=" * 50)

# 建立 Capital Broker (會自動用 Mock)
broker2 = BrokerFactory.create("capital")
print(f"連線: {broker2.connect('F123404431', '@1E3t4h1a9n9@')}")
print(f"券商: {broker2.name}")

# 取得報價
quote2 = broker2.get_quote("TXF")
print(f"\n報價:")
print(f"  商品: {quote2.symbol}")
print(f"  價格: {quote2.close}")

print("\n" + "=" * 50)
print("完成！")
print("=" * 50)
