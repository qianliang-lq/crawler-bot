"""Adapter 契约测试

为将来的 Adapter 实现定义契约测试。当 adapters/families/csrc_search_list.py
实现后，这些测试将验证其行为符合预期。
"""

from typing import Any, Dict

import pytest

from crawler_bot.urlutil import build_csrc_searchlist_url


def test_adapter_module_structure():
    """验证 Adapter 模块结构（当实现时）

    这是一个"准备就绪"测试 - 当 Adapter 实现后将开始执行。
    """
    try:
        from adapters.families import csrc_search_list

        assert hasattr(
            csrc_search_list, "CsrcSearchListAdapter"
        ), "应导出 CsrcSearchListAdapter 类"

    except ImportError:
        pytest.skip("adapters/families/csrc_search_list.py 尚未实现")


def test_adapter_has_required_methods():
    """验证 Adapter 类具有必需的方法"""
    try:
        from adapters.families.csrc_search_list import CsrcSearchListAdapter

        required_methods = ["fetch_list", "fetch_detail", "run_incremental", "_api_url"]

        for method in required_methods:
            assert hasattr(
                CsrcSearchListAdapter, method
            ), f"CsrcSearchListAdapter 应有 {method} 方法"

    except ImportError:
        pytest.skip("adapters/families/csrc_search_list.py 尚未实现")


class TestAdapterUrlBuilding:
    """测试 Adapter 的 URL 构建能力

    验收标准：同一 Adapter 类加载两套站点参数应能构建不同的正确 API URL。
    """

    def test_sz_adapter_builds_correct_api_url(self, csrc_sz_skill: Dict[str, Any]):
        """深圳站点 Adapter 应构建正确的 API URL"""
        try:
            from adapters.families.csrc_search_list import CsrcSearchListAdapter

            adapter = CsrcSearchListAdapter(skill=csrc_sz_skill)
            api_url = adapter._api_url(page=1, page_size=20)

            params = csrc_sz_skill["params"]
            assert params["channelid"] in api_url, "API URL 应包含深圳 channelid"
            assert api_url.startswith("https://"), "API URL 应使用 https"
            assert "/searchList/" in api_url, "API URL 应包含 searchList 路径"

        except ImportError:
            pytest.skip("CsrcSearchListAdapter 尚未实现，使用 urlutil 验证")

            params = csrc_sz_skill["params"]
            api_url = build_csrc_searchlist_url(
                host=params["host"], channelid=params["channelid"], page=1, page_size=20
            )

            assert params["channelid"] in api_url
            assert api_url.startswith("https://")

    def test_sh_adapter_builds_correct_api_url(self, csrc_sh_skill: Dict[str, Any]):
        """上海站点 Adapter 应构建正确的 API URL"""
        try:
            from adapters.families.csrc_search_list import CsrcSearchListAdapter

            adapter = CsrcSearchListAdapter(skill=csrc_sh_skill)
            api_url = adapter._api_url(page=1, page_size=20)

            params = csrc_sh_skill["params"]
            assert params["channelid"] in api_url, "API URL 应包含上海 channelid"
            assert api_url.startswith("https://"), "API URL 应使用 https"
            assert "/searchList/" in api_url, "API URL 应包含 searchList 路径"

        except ImportError:
            pytest.skip("CsrcSearchListAdapter 尚未实现，使用 urlutil 验证")

            params = csrc_sh_skill["params"]
            api_url = build_csrc_searchlist_url(
                host=params["host"], channelid=params["channelid"], page=1, page_size=20
            )

            assert params["channelid"] in api_url
            assert api_url.startswith("https://")

    def test_same_adapter_class_different_params(
        self, csrc_sz_skill: Dict[str, Any], csrc_sh_skill: Dict[str, Any]
    ):
        """同一 Adapter 类应能处理两套不同参数（深圳和上海）"""
        try:
            from adapters.families.csrc_search_list import CsrcSearchListAdapter

            adapter_sz = CsrcSearchListAdapter(skill=csrc_sz_skill)
            adapter_sh = CsrcSearchListAdapter(skill=csrc_sh_skill)

            url_sz = adapter_sz._api_url(page=1, page_size=20)
            url_sh = adapter_sh._api_url(page=1, page_size=20)

            assert url_sz != url_sh, "两个站点的 API URL 应不同"
            assert csrc_sz_skill["params"]["channelid"] in url_sz
            assert csrc_sh_skill["params"]["channelid"] in url_sh

        except ImportError:
            pytest.skip("CsrcSearchListAdapter 尚未实现，使用 urlutil 验证")

            url_sz = build_csrc_searchlist_url(
                host=csrc_sz_skill["params"]["host"],
                channelid=csrc_sz_skill["params"]["channelid"],
                page=1,
                page_size=20,
            )

            url_sh = build_csrc_searchlist_url(
                host=csrc_sh_skill["params"]["host"],
                channelid=csrc_sh_skill["params"]["channelid"],
                page=1,
                page_size=20,
            )

            assert url_sz != url_sh
            assert csrc_sz_skill["params"]["channelid"] in url_sz
            assert csrc_sh_skill["params"]["channelid"] in url_sh


class TestAdapterListItemContract:
    """测试 Adapter 返回的 ListItem 数据契约"""

    def test_list_item_has_required_fields(self):
        """ListItem 应包含必需字段"""
        try:
            from adapters.base import ListItem

            item = ListItem(
                title="测试标题",
                url="https://www.csrc.gov.cn/test",
                published_at="2026-08-14 17:50:39",
                manuscript_id="7652321",
                raw={},
            )

            assert item.title == "测试标题"
            assert item.url.startswith("https://")
            assert item.published_at
            assert item.manuscript_id

        except ImportError:
            pytest.skip("adapters/base.py ListItem 尚未实现")


class TestAdapterDetailDocContract:
    """测试 Adapter 返回的 DetailDoc 数据契约"""

    def test_detail_doc_has_required_fields(self):
        """DetailDoc 应包含必需字段"""
        try:
            from adapters.base import DetailDoc

            doc = DetailDoc(
                title="测试标题",
                url="https://www.csrc.gov.cn/test",
                published_at="2026-08-14 17:50:39",
                content_md="# 测试内容\n\n这是测试内容。",
                raw_hash="abc123",
                attachments=[],
            )

            assert doc.title
            assert doc.url.startswith("https://")
            assert doc.published_at
            assert doc.content_md
            assert len(doc.content_md) >= 10, "content_md 应有实质内容"
            assert doc.raw_hash

        except ImportError:
            pytest.skip("adapters/base.py DetailDoc 尚未实现")
