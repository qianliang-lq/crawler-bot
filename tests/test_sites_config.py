"""站点配置测试

验证 sites/*/SKILL.yaml 包含所有必需字段并符合规范。
"""

from pathlib import Path
from typing import Any, Dict

import pytest

REQUIRED_TOP_LEVEL_KEYS = [
    "site_id",
    "family",
    "params",
    "list_rule",
    "rate_limit",
    "tests",
]


def test_csrc_sz_site_exists(repo_root: Path):
    """深圳专员办站点配置文件存在"""
    site_path = repo_root / "sites" / "csrc-szzyb-0599" / "SKILL.yaml"
    assert site_path.exists(), "深圳专员办 SKILL.yaml 不存在"


def test_csrc_sh_site_exists(repo_root: Path):
    """上海专员办站点配置文件存在"""
    site_path = repo_root / "sites" / "csrc-shzyb-3fde" / "SKILL.yaml"
    assert site_path.exists(), "上海专员办 SKILL.yaml 不存在"


@pytest.mark.parametrize("site_id", ["csrc-szzyb-0599", "csrc-shzyb-3fde"])
def test_site_has_required_keys(load_site_skill, site_id: str):
    """站点配置包含所有必需的顶级键"""
    skill = load_site_skill(site_id)

    for key in REQUIRED_TOP_LEVEL_KEYS:
        assert key in skill, f"{site_id} 缺少必需键: {key}"


@pytest.mark.parametrize("site_id", ["csrc-szzyb-0599", "csrc-shzyb-3fde"])
def test_site_family_is_csrc_search_list(load_site_skill, site_id: str):
    """两个站点都应使用同一个 csrc_search_list family"""
    skill = load_site_skill(site_id)
    assert (
        skill["family"] == "csrc_search_list"
    ), f"{site_id} family 应为 'csrc_search_list'，实际: {skill['family']}"


@pytest.mark.parametrize("site_id", ["csrc-szzyb-0599", "csrc-shzyb-3fde"])
def test_site_has_valid_params(load_site_skill, site_id: str):
    """站点 params 包含 CSRC 必需字段"""
    skill = load_site_skill(site_id)
    params = skill["params"]

    required_params = ["host", "org_prefix", "column_code", "channelid"]
    for param in required_params:
        assert param in params, f"{site_id} params 缺少: {param}"
        assert params[param], f"{site_id} params.{param} 不能为空"


@pytest.mark.parametrize("site_id", ["csrc-szzyb-0599", "csrc-shzyb-3fde"])
def test_site_has_list_rule_with_api_path(load_site_skill, site_id: str):
    """站点 list_rule 包含 api_path"""
    skill = load_site_skill(site_id)
    list_rule = skill["list_rule"]

    assert "api_path" in list_rule, f"{site_id} list_rule 缺少 api_path"
    assert (
        "{channelid}" in list_rule["api_path"]
    ), f"{site_id} list_rule.api_path 应包含 {{channelid}} 占位符"


@pytest.mark.parametrize("site_id", ["csrc-szzyb-0599", "csrc-shzyb-3fde"])
def test_site_rate_limit_in_compliance_range(load_site_skill, site_id: str):
    """站点 rate_limit.rps 在合规范围内（0.2-0.5）"""
    skill = load_site_skill(site_id)
    rate_limit = skill["rate_limit"]

    assert "rps" in rate_limit, f"{site_id} 缺少 rate_limit.rps"

    rps = rate_limit["rps"]
    assert (
        0.2 <= rps <= 0.5
    ), f"{site_id} rate_limit.rps 应在 0.2-0.5 范围内，实际: {rps}"


@pytest.mark.parametrize("site_id", ["csrc-szzyb-0599", "csrc-shzyb-3fde"])
def test_site_has_tests_config(load_site_skill, site_id: str):
    """站点配置包含 tests 配置（golden_* 字段）"""
    skill = load_site_skill(site_id)
    tests = skill["tests"]

    assert "golden_list_url" in tests, f"{site_id} tests 缺少 golden_list_url"


def test_sz_and_sh_params_differ_correctly(
    csrc_sz_skill: Dict[str, Any], csrc_sh_skill: Dict[str, Any]
):
    """验证深圳和上海站点的参数差异符合预期"""
    sz_params = csrc_sz_skill["params"]
    sh_params = csrc_sh_skill["params"]

    assert sz_params["host"] == sh_params["host"], "两站点应共享同一 host"

    assert sz_params["org_prefix"] != sh_params["org_prefix"], "org_prefix 应不同"
    assert sz_params["column_code"] != sh_params["column_code"], "column_code 应不同"
    assert sz_params["channelid"] != sh_params["channelid"], "channelid 应不同"

    assert sz_params["org_prefix"] == "szzyb"
    assert sh_params["org_prefix"] == "shzyb"


def test_fixture_paths_are_repo_relative(csrc_sz_skill: Dict[str, Any]):
    """验证 fixture 路径不再指向 /workspace/briefs（如有配置）"""
    if "fixture_list_json" in csrc_sz_skill.get("tests", {}):
        fixture_path = csrc_sz_skill["tests"]["fixture_list_json"]
        assert not fixture_path.startswith(
            "/workspace/briefs"
        ), f"fixture 路径应为仓库相对路径，而非绝对路径: {fixture_path}"
