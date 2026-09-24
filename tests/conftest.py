"""pytest 配置和共享 fixtures"""

import json
from pathlib import Path
from typing import Any, Dict

import pytest
import yaml


@pytest.fixture(scope="session")
def repo_root() -> Path:
    """返回仓库根目录路径"""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def fixtures_dir(repo_root: Path) -> Path:
    """返回 fixtures 目录路径"""
    return repo_root / "tests" / "fixtures"


@pytest.fixture
def load_site_skill(repo_root: Path):
    """加载站点 SKILL.yaml 配置的工厂函数

    Usage:
        def test_something(load_site_skill):
            skill = load_site_skill("csrc-szzyb-0599")
            assert skill["family"] == "csrc_search_list"
    """

    def _load(site_id: str) -> Dict[str, Any]:
        skill_path = repo_root / "sites" / site_id / "SKILL.yaml"
        with open(skill_path, encoding="utf-8") as f:
            return yaml.safe_load(f)

    return _load


@pytest.fixture
def load_fixture_json(fixtures_dir: Path):
    """加载 fixture JSON 文件的工厂函数

    Usage:
        def test_parse(load_fixture_json):
            data = load_fixture_json("csrc-szzyb-0599/csrc_searchList_sample.json")
            assert data["data"]["total"] > 0
    """

    def _load(relative_path: str) -> Dict[str, Any]:
        fixture_path = fixtures_dir / relative_path
        with open(fixture_path, encoding="utf-8") as f:
            return json.load(f)

    return _load


@pytest.fixture
def load_fixture_html(fixtures_dir: Path):
    """加载 fixture HTML 文件的工厂函数"""

    def _load(relative_path: str) -> str:
        fixture_path = fixtures_dir / relative_path
        with open(fixture_path, encoding="utf-8") as f:
            return f.read()

    return _load


@pytest.fixture(scope="session")
def csrc_sz_skill(repo_root: Path) -> Dict[str, Any]:
    """深圳专员办站点配置（会话级缓存）"""
    with open(
        repo_root / "sites" / "csrc-szzyb-0599" / "SKILL.yaml", encoding="utf-8"
    ) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def csrc_sh_skill(repo_root: Path) -> Dict[str, Any]:
    """上海专员办站点配置（会话级缓存）"""
    with open(
        repo_root / "sites" / "csrc-shzyb-3fde" / "SKILL.yaml", encoding="utf-8"
    ) as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def csrc_searchlist_sample(fixtures_dir: Path) -> Dict[str, Any]:
    """深圳 searchList 示例数据（会话级缓存）"""
    with open(
        fixtures_dir / "csrc-szzyb-0599" / "csrc_searchList_sample.json",
        encoding="utf-8",
    ) as f:
        return json.load(f)
