"""技能配置契约测试

验证 skills/*/SKILL.md 符合标准格式和必需字段要求。
"""

import re
from pathlib import Path


def test_all_skills_have_frontmatter(repo_root: Path):
    """每个 skill 的 SKILL.md 必须包含 YAML frontmatter"""
    skills_dir = repo_root / "skills"
    skill_dirs = [
        d for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()
    ]

    assert len(skill_dirs) > 0, "应至少有一个 skill 目录"

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")

        assert content.startswith(
            "---\n"
        ), f"{skill_dir.name}/SKILL.md 必须以 YAML frontmatter 开始"

        frontmatter_end = content.find("\n---\n", 4)
        assert frontmatter_end > 0, f"{skill_dir.name}/SKILL.md frontmatter 未正确闭合"


def test_all_skills_have_name_and_description(repo_root: Path):
    """每个 skill 的 frontmatter 必须包含 name 和 description 字段"""
    skills_dir = repo_root / "skills"
    skill_dirs = [
        d for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()
    ]

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")

        frontmatter_match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
        assert frontmatter_match, f"{skill_dir.name}/SKILL.md 缺少有效的 frontmatter"

        frontmatter = frontmatter_match.group(1)

        assert re.search(
            r"^name:", frontmatter, re.MULTILINE
        ), f"{skill_dir.name}/SKILL.md frontmatter 缺少 'name' 字段"
        assert re.search(
            r"^description:", frontmatter, re.MULTILINE
        ), f"{skill_dir.name}/SKILL.md frontmatter 缺少 'description' 字段"


def test_skill_descriptions_follow_use_this_when_pattern(repo_root: Path):
    """skill description 应以 'Use this when' 开头（符合约定）"""
    skills_dir = repo_root / "skills"
    skill_dirs = [
        d for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()
    ]

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        content = skill_md.read_text(encoding="utf-8")

        frontmatter_match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
        assert frontmatter_match

        frontmatter = frontmatter_match.group(1)

        desc_match = re.search(
            r'^description:\s*["\'](.+?)["\']', frontmatter, re.MULTILINE
        )
        if desc_match:
            description = desc_match.group(1)
            assert description.startswith(
                "Use this when"
            ), f"{skill_dir.name}/SKILL.md description 应以 'Use this when' 开头，实际: {description[:50]}"


def test_expected_skills_exist(repo_root: Path):
    """验证关键 skills 目录存在"""
    expected_skills = [
        "intake-excel",
        "probe-site",
        "skillsmith-reg",
        "adapter-codegen",
        "detail-to-markdown",
        "golden-test",
        "scheduler-incremental",
        "pdf-extract",
        "export-query",
    ]

    skills_dir = repo_root / "skills"

    for skill_name in expected_skills:
        skill_path = skills_dir / skill_name / "SKILL.md"
        assert skill_path.exists(), f"缺少必需的 skill: {skill_name}/SKILL.md"
