"""URL 工具函数测试

测试 crawler_bot.urlutil 中的 URL 构建和规范化函数。
"""

from crawler_bot.urlutil import (
    build_csrc_searchlist_url,
    build_detail_url,
    normalize_url,
)


class TestNormalizeUrl:
    """测试 URL 规范化"""

    def test_protocol_relative_to_https(self):
        """协议相对 URL 应转换为 https"""
        url = "//www.csrc.gov.cn/szzyb/c101700/content.shtml"
        result = normalize_url(url)
        assert result == "https://www.csrc.gov.cn/szzyb/c101700/content.shtml"

    def test_already_https_unchanged(self):
        """已经是 https 的 URL 应保持不变"""
        url = "https://www.csrc.gov.cn/test"
        result = normalize_url(url)
        assert result == url

    def test_empty_string_returns_empty(self):
        """空字符串应返回空字符串"""
        assert normalize_url("") == ""

    def test_http_url_unchanged(self):
        """http URL 保持不变（不强制升级）"""
        url = "http://example.com/test"
        result = normalize_url(url)
        assert result == url


class TestBuildCsrcSearchlistUrl:
    """测试 CSRC searchList API URL 构建"""

    def test_build_sz_list_url(self, csrc_sz_skill):
        """构建深圳专员办 searchList URL"""
        params = csrc_sz_skill["params"]
        url = build_csrc_searchlist_url(
            host=params["host"],
            channelid=params["channelid"],
            page=1,
            page_size=20,
        )

        assert url.startswith("https://www.csrc.gov.cn/searchList/")
        assert params["channelid"] in url
        assert "_isAgg=false" in url
        assert "_isJson=true" in url
        assert "_pageSize=20" in url
        assert "page=1" in url

    def test_build_sh_list_url(self, csrc_sh_skill):
        """构建上海专员办 searchList URL"""
        params = csrc_sh_skill["params"]
        url = build_csrc_searchlist_url(
            host=params["host"],
            channelid=params["channelid"],
            page=1,
            page_size=20,
        )

        assert url.startswith("https://www.csrc.gov.cn/searchList/")
        assert params["channelid"] in url
        assert "_isAgg=false" in url
        assert "_isJson=true" in url

    def test_different_page_numbers(self):
        """测试不同页码"""
        url_page1 = build_csrc_searchlist_url(
            "www.csrc.gov.cn", "test-channel-id", page=1
        )
        url_page3 = build_csrc_searchlist_url(
            "www.csrc.gov.cn", "test-channel-id", page=3
        )

        assert "page=1" in url_page1
        assert "page=3" in url_page3
        assert url_page1 != url_page3

    def test_different_page_sizes(self):
        """测试不同每页大小"""
        url_20 = build_csrc_searchlist_url("www.csrc.gov.cn", "test-id", page_size=20)
        url_50 = build_csrc_searchlist_url("www.csrc.gov.cn", "test-id", page_size=50)

        assert "_pageSize=20" in url_20
        assert "_pageSize=50" in url_50

    def test_matches_golden_url_from_skill(self, csrc_sz_skill):
        """构建的 URL 应匹配 skill 中的 golden_list_url 模式"""
        params = csrc_sz_skill["params"]
        golden_url = csrc_sz_skill["tests"]["golden_list_url"]

        built_url = build_csrc_searchlist_url(
            host=params["host"],
            channelid=params["channelid"],
            page=1,
            page_size=5,
        )

        assert params["channelid"] in built_url
        assert params["channelid"] in golden_url

        assert built_url.split("?")[0] == golden_url.split("?")[0], "路径部分应匹配"


class TestBuildDetailUrl:
    """测试详情页 URL 构建"""

    def test_build_sz_detail_url(self, csrc_sz_skill):
        """构建深圳专员办详情页 URL"""
        params = csrc_sz_skill["params"]
        url = build_detail_url(
            host=params["host"],
            org_prefix=params["org_prefix"],
            column_code=params["column_code"],
            manuscript_id="7652321",
        )

        expected = "https://www.csrc.gov.cn/szzyb/c101700/c7652321/content.shtml"
        assert url == expected

    def test_build_sh_detail_url(self, csrc_sh_skill):
        """构建上海专员办详情页 URL"""
        params = csrc_sh_skill["params"]
        url = build_detail_url(
            host=params["host"],
            org_prefix=params["org_prefix"],
            column_code=params["column_code"],
            manuscript_id="1234567",
        )

        assert url.startswith("https://www.csrc.gov.cn/shzyb/")
        assert "/c101682/c1234567/content.shtml" in url

    def test_manuscript_id_formatting(self):
        """验证 manuscriptId 前缀 'c' 的添加"""
        url = build_detail_url("www.csrc.gov.cn", "szzyb", "c101700", "7652321")

        assert "/c7652321/" in url, "manuscriptId 应加 'c' 前缀"
