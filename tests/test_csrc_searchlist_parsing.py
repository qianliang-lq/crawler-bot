"""CSRC searchList 列表数据解析测试

使用现有 fixture 验证 JSON 列表解析逻辑和字段提取。
"""

import re
from typing import Any, Dict

import pytest

from crawler_bot.urlutil import normalize_url


def test_fixture_loads_successfully(csrc_searchlist_sample: Dict[str, Any]):
    """验证 fixture JSON 成功加载"""
    assert csrc_searchlist_sample is not None
    assert "data" in csrc_searchlist_sample


def test_list_has_positive_total(csrc_searchlist_sample: Dict[str, Any]):
    """列表数据应包含大于 0 的 total 字段"""
    data = csrc_searchlist_sample["data"]
    assert "total" in data
    assert data["total"] > 0, f"total 应 > 0，实际: {data['total']}"


def test_list_has_results_array(csrc_searchlist_sample: Dict[str, Any]):
    """列表数据应包含 results 数组"""
    data = csrc_searchlist_sample["data"]
    assert "results" in data
    assert isinstance(data["results"], list)
    assert len(data["results"]) > 0, "results 数组不应为空"


@pytest.mark.parametrize("item_index", [0, 1, 2, 3, 4])
def test_list_items_have_required_fields(
    csrc_searchlist_sample: Dict[str, Any], item_index: int
):
    """列表中前 5 项应包含必需字段：title、url、publishedTimeStr、manuscriptId"""
    results = csrc_searchlist_sample["data"]["results"]

    if item_index >= len(results):
        pytest.skip(f"结果集不足 {item_index + 1} 项")

    item = results[item_index]

    assert "title" in item, f"项 {item_index} 缺少 title"
    assert item["title"], f"项 {item_index} title 不应为空"

    assert "url" in item, f"项 {item_index} 缺少 url"
    assert item["url"], f"项 {item_index} url 不应为空"

    assert "publishedTimeStr" in item, f"项 {item_index} 缺少 publishedTimeStr"
    assert item["publishedTimeStr"], f"项 {item_index} publishedTimeStr 不应为空"

    assert "manuscriptId" in item, f"项 {item_index} 缺少 manuscriptId"
    assert item["manuscriptId"], f"项 {item_index} manuscriptId 不应为空"


def test_published_time_format_is_parseable(csrc_searchlist_sample: Dict[str, Any]):
    """验证 publishedTimeStr 格式可解析（YYYY-MM-DD HH:MM:SS）"""
    results = csrc_searchlist_sample["data"]["results"]

    time_pattern = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$")

    for idx, item in enumerate(results[:5]):
        pub_time = item.get("publishedTimeStr", "")
        assert time_pattern.match(
            pub_time
        ), f"项 {idx} publishedTimeStr 格式不正确: {pub_time}"


def test_url_normalization_from_protocol_relative(
    csrc_searchlist_sample: Dict[str, Any],
):
    """验证协议相对 URL（//host/...）能正确规范化为 https://"""
    results = csrc_searchlist_sample["data"]["results"]

    for idx, item in enumerate(results[:5]):
        raw_url = item["url"]
        normalized = normalize_url(raw_url)

        assert normalized.startswith(
            "https://"
        ), f"项 {idx} URL 应规范化为 https://，实际: {normalized}"

        assert (
            "//" not in normalized[8:]
        ), f"项 {idx} 规范化后不应包含双斜杠: {normalized}"


def test_manuscript_id_is_present_and_non_empty(csrc_searchlist_sample: Dict[str, Any]):
    """验证所有项的 manuscriptId 存在且非空"""
    results = csrc_searchlist_sample["data"]["results"]

    for idx, item in enumerate(results[:5]):
        manuscript_id = item.get("manuscriptId")
        assert manuscript_id, f"项 {idx} manuscriptId 不应为空或 None"

        assert str(manuscript_id).isdigit() or isinstance(
            manuscript_id, (int, str)
        ), f"项 {idx} manuscriptId 格式异常: {manuscript_id}"


def test_channel_info_fields_present(csrc_searchlist_sample: Dict[str, Any]):
    """验证频道信息字段存在"""
    results = csrc_searchlist_sample["data"]["results"]
    first_item = results[0]

    expected_fields = ["channelId", "channelName", "channelCodeName"]

    for field in expected_fields:
        assert field in first_item, f"首项应包含 {field} 字段"


def test_content_html_field_exists(csrc_searchlist_sample: Dict[str, Any]):
    """验证 contentHtml 字段存在（可能为空或包含预览链接）"""
    results = csrc_searchlist_sample["data"]["results"]
    first_item = results[0]

    assert "contentHtml" in first_item, "应包含 contentHtml 字段"


def test_url_matches_expected_csrc_pattern(csrc_searchlist_sample: Dict[str, Any]):
    """验证 URL 符合 CSRC 详情页模式"""
    results = csrc_searchlist_sample["data"]["results"]

    csrc_pattern = re.compile(r"//www\.csrc\.gov\.cn/[a-z]+/c\d+/c\d+/content\.shtml")

    for idx, item in enumerate(results[:5]):
        url = item["url"]
        assert csrc_pattern.match(url), f"项 {idx} URL 不符合 CSRC 模式: {url}"
