"""HANDOFF.md 检查清单项测试

验证 HANDOFF.md 中已标记为完成的事项。
"""

from pathlib import Path


def test_six_main_skills_discoverable(repo_root: Path):
    """六个主要 skills 的 SKILL.md 在仓库内可被 Agent 发现"""
    main_skills = [
        "intake-excel",
        "probe-site",
        "skillsmith-reg",
        "adapter-codegen",
        "detail-to-markdown",
        "golden-test",
    ]

    skills_dir = repo_root / "skills"

    for skill_name in main_skills:
        skill_md = skills_dir / skill_name / "SKILL.md"
        assert skill_md.exists(), f"主要 skill {skill_name}/SKILL.md 应存在"

        content = skill_md.read_text(encoding="utf-8")
        assert len(content) > 100, f"{skill_name}/SKILL.md 应包含实质内容"


def test_both_site_yamls_are_human_readable(repo_root: Path):
    """两份 site SKILL.yaml 应人类可读"""
    import yaml

    sz_path = repo_root / "sites" / "csrc-szzyb-0599" / "SKILL.yaml"
    sh_path = repo_root / "sites" / "csrc-shzyb-3fde" / "SKILL.yaml"

    assert sz_path.exists()
    assert sh_path.exists()

    with open(sz_path, encoding="utf-8") as f:
        sz_data = yaml.safe_load(f)
        assert sz_data is not None
        assert isinstance(sz_data, dict)

    with open(sh_path, encoding="utf-8") as f:
        sh_data = yaml.safe_load(f)
        assert sh_data is not None
        assert isinstance(sh_data, dict)


def test_both_sites_have_csrc_search_list_family(repo_root: Path):
    """两份 site SKILL.yaml 的 family 均为 csrc_search_list"""
    import yaml

    sz_path = repo_root / "sites" / "csrc-szzyb-0599" / "SKILL.yaml"
    sh_path = repo_root / "sites" / "csrc-shzyb-3fde" / "SKILL.yaml"

    with open(sz_path, encoding="utf-8") as f:
        sz_data = yaml.safe_load(f)
        assert sz_data["family"] == "csrc_search_list"

    with open(sh_path, encoding="utf-8") as f:
        sh_data = yaml.safe_load(f)
        assert sh_data["family"] == "csrc_search_list"


def test_experiment_doc_exists(repo_root: Path):
    """实验文档应已链到 docs"""
    exp_doc = repo_root / "docs" / "experiments" / "2026-09-24-csrc-sz-sh.md"

    assert exp_doc.exists(), "实验文档应存在"

    content = exp_doc.read_text(encoding="utf-8")
    assert len(content) > 200, "实验文档应包含实质内容"
