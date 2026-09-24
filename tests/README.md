# 测试套件

监管源采集数字员工（M0）的测试套件。

## 运行测试

### 安装依赖

```bash
pip install -e ".[test]"
```

或者只安装测试依赖：

```bash
pip install pytest pytest-cov pyyaml
```

### 运行所有离线测试（默认）

```bash
pytest
```

### 运行特定测试文件

```bash
pytest tests/test_sites_config.py
pytest tests/test_url_utils.py
```

### 运行带覆盖率报告

```bash
pytest --cov=crawler_bot --cov-report=term-missing
```

### 查看详细输出

```bash
pytest -v
pytest -vv  # 更详细
```

## 测试分类

### 离线测试（默认运行）

所有不需要网络访问的测试，使用本地 fixtures：

- `test_skills_contract.py` - 验证 skills 配置格式
- `test_sites_config.py` - 验证站点 YAML 配置
- `test_csrc_searchlist_parsing.py` - 使用 fixture JSON 测试列表解析
- `test_url_utils.py` - URL 工具函数单元测试
- `test_adapter_contract.py` - Adapter 接口契约测试（准备就绪）
- `test_handoff_checklist.py` - HANDOFF.md 检查清单验证

### 在线测试（标记为 @pytest.mark.online，默认跳过）

需要网络访问的测试，需明确启用：

```bash
pytest -m online
```

**注意**: 在线测试默认被跳过，符合 CI 无需外网访问的原则。

## Fixtures

测试使用的示例数据位于 `tests/fixtures/`：

```
tests/fixtures/
└── csrc-szzyb-0599/
    ├── csrc_searchList_sample.json  # 深圳专员办列表 JSON 示例
    ├── csrc_detail_sample.html      # 详情页 HTML 示例
    ├── csrc_sz.html                 # 深圳壳页示例
    ├── csrc_sh.html                 # 上海壳页示例
    └── common_list.js               # 列表 JS 脚本示例
```

## 测试内容概览

### A. 配置契约测试
- ✅ Skills 的 SKILL.md 包含必需的 YAML frontmatter
- ✅ 每个 skill 有 `name` 和 `description` 字段
- ✅ Description 遵循 "Use this when..." 模式
- ✅ 站点 SKILL.yaml 包含必需键（site_id, family, params, list_rule, rate_limit, tests）
- ✅ 两站点共享同一 family `csrc_search_list`
- ✅ Rate limit 在合规范围 0.2-0.5 rps

### B. 列表解析测试（使用 fixture）
- ✅ 加载 csrc_searchList_sample.json
- ✅ 验证 `data.total` > 0
- ✅ 前 5 项包含 title, url, publishedTimeStr, manuscriptId
- ✅ 时间格式可解析（YYYY-MM-DD HH:MM:SS）
- ✅ URL 规范化：`//host/...` → `https://host/...`

### C. URL 工具测试
- ✅ 协议相对路径规范化
- ✅ 为深圳/上海站点构建正确的 searchList API URL
- ✅ 详情页 URL 构建（含 manuscriptId 格式化）
- ✅ 不同页码和页面大小参数

### D. Adapter 契约测试（准备就绪）
- ⏳ 当 `adapters/families/csrc_search_list.py` 实现后：
  - 验证 CsrcSearchListAdapter 类存在
  - 验证必需方法（fetch_list, fetch_detail, run_incremental, _api_url）
  - 同一 Adapter 类加载深圳/上海两套参数能构建不同的正确 URL
  - ListItem 和 DetailDoc 数据契约

### E. HANDOFF 检查清单
- ✅ 六个主要 skills 可被 Agent 发现
- ✅ 两份 site YAML 人类可读且 family 均为 csrc_search_list
- ✅ 实验文档已存在于 docs/

## 添加新测试

1. 在 `tests/` 下创建 `test_*.py` 文件
2. 使用 `conftest.py` 中的 fixtures
3. 离线测试：使用 `tests/fixtures/` 中的数据
4. 在线测试：添加 `@pytest.mark.online` 标记

示例：

```python
import pytest

def test_something_offline(load_fixture_json):
    """离线测试：使用 fixture"""
    data = load_fixture_json("csrc-szzyb-0599/csrc_searchList_sample.json")
    assert data["data"]["total"] > 0

@pytest.mark.online
def test_something_online():
    """在线测试：需要网络"""
    # 仅在显式运行 pytest -m online 时执行
    pass
```

## CI/CD 集成

默认 `pytest` 命令只运行离线测试，适合无外网访问的 CI 环境。

要在 CI 中启用在线测试（如果有稳定出口）：

```bash
pytest -m online
```

## 限制与注意事项

1. **不实现生产 Adapter** - 本测试套件不包含完整 Adapter 实现，仅提供契约测试和 URL 构建辅助函数
2. **无实时爬取** - 默认测试不访问 CSRC 真实 API（遵守 rate_limit 和合规要求）
3. **Adapter 契约测试** - 使用 `pytest.importorskip` 或 `pytest.skip`，当 Adapter 实现后自动激活
4. **Fixture 路径** - 站点 YAML 中的 fixture 路径应为仓库相对路径，不是绝对路径

## 测试通过标准

```bash
$ pytest
======================== test session starts =========================
collected 50+ items

tests/test_skills_contract.py ............           [ XX%]
tests/test_sites_config.py ...................       [ XX%]
tests/test_csrc_searchlist_parsing.py ............   [ XX%]
tests/test_url_utils.py .................             [ XX%]
tests/test_adapter_contract.py ssssss                 [ XX%]  # skipped (Adapter 未实现)
tests/test_handoff_checklist.py ....                 [100%]

=================== XX passed, 6 skipped in X.XXs ===================
```

其中 skipped 测试为 Adapter 契约测试，等待 `adapters/families/csrc_search_list.py` 实现后自动激活。
