# Delta Data SDK — 高频行情数据查询

## 概述

高频行情数据查询 SDK，为量化交易提供统一的数据库访问接口。
纯查询层，不含业务逻辑 (特征计算、归一化等在各项目自行实现)。

## 安装

```bash
# 从 GitHub 安装
pip install git+https://github.com/0xLian117/delta_data_sdk.git

# 本地开发安装 (推荐)
pip install -e code/delta_data_sdk/
```

## DSN

```python
DSN = "postgresql://deltadb:delta_data@10.246.1.175:5432/deltadb"
```

## API 参考

### DeltaDB — 同步查询

```python
from delta_data import DeltaDB

db = DeltaDB(DSN)
db.connect()

# 元数据
db.list_symbols()                    # 所有可用品种
db.list_trading_days(symbol)         # 品种的交易日
db.get_stats()                       # 数据统计
db.get_info()                        # 品种详情表

# 数据查询（返回 DataFrame）
db.query(symbol, start, end)         # 按时间范围查询
db.query_day(symbol, trading_day)    # 按交易日查询
db.query_multi(symbols, start, end)  # 并发查询多品种
db.query_trades(symbol, start, end)  # 查询逐笔成交

# 便捷方法
db.head(symbol)                      # 前 N 条
db.tail(symbol)                      # 后 N 条
db.resample(symbol, start, end, '1min')  # 生成 K 线

db.close()
```

### 存储层（高级用户）

```python
from delta_data import SnapshotStore, TradeStore

# 异步存储
store = SnapshotStore(dsn)
await store.connect()
snapshots = await store.query(symbol, start, end)
await store.close()

# 同步存储
from delta_data import SyncSnapshotStore
store = SyncSnapshotStore(dsn)
store.connect()
snapshots = store.query(symbol, start, end)
store.close()
```

## 支持的交易所

| 交易所 | 代码 | 品种示例 |
|--------|------|----------|
| 上期所 | SHFE | AU, CU, RB, AG |
| 上期能源 | INE | SC, NR, LU |
| 大商所 | DCE | I, J, JM, M, P |
| 郑商所 | CZCE | MA, SA, TA, FG |
| 广期所 | GFEX | SI, LC |
| 中金所 | CFFEX | IF, IH, IC, IM |
| 币安 | BINANCE | BTCUSDT, ETHUSDT |

## 数据库表结构

| 表名 | 用途 |
|------|------|
| `market_snapshots` | 盘口快照（行情+订单簿）— TimescaleDB hypertable |
| `market_trades` | 逐笔成交 |
| `instruments` | 品种元数据 |

## 配置工具

```python
from delta_data import (
    get_exchange,         # AU -> SHFE
    get_instrument_name,  # AU -> 黄金
    parse_instrument_id,  # au2406 -> {underlying, month}
    get_trading_sessions, # 获取交易时段
    has_night_session,    # 判断是否有夜盘
)
```
