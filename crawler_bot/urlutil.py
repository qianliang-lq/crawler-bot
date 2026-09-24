"""URL 构建和规范化工具

提供 CSRC searchList API URL 构建和协议相对路径规范化功能。
"""


def normalize_url(url: str) -> str:
    """将协议相对 URL 规范化为 https 绝对 URL

    Args:
        url: 可能包含协议相对路径的 URL（如 //www.csrc.gov.cn/...）

    Returns:
        规范化后的 https:// URL

    Examples:
        >>> normalize_url("//www.csrc.gov.cn/szzyb/c101700/content.shtml")
        'https://www.csrc.gov.cn/szzyb/c101700/content.shtml'
        >>> normalize_url("https://www.csrc.gov.cn/test")
        'https://www.csrc.gov.cn/test'
    """
    if not url:
        return url

    if url.startswith("//"):
        return "https:" + url
    return url


def build_csrc_searchlist_url(
    host: str,
    channelid: str,
    page: int = 1,
    page_size: int = 20,
    api_path_template: str = "/searchList/{channelid}",
) -> str:
    """为 CSRC searchList API 构建完整 URL

    根据站点 Skill 参数构建 searchList JSON API 的完整请求 URL。

    Args:
        host: API 主机名（如 www.csrc.gov.cn）
        channelid: 频道 ID（从站点 SKILL.yaml params.channelid 获取）
        page: 页码（从 1 开始）
        page_size: 每页大小
        api_path_template: API 路径模板（默认 /searchList/{channelid}）

    Returns:
        完整的 API URL，包含查询参数

    Examples:
        >>> build_csrc_searchlist_url(
        ...     "www.csrc.gov.cn",
        ...     "059986f6f4834fe6ae61cb76bd9ef23b",
        ...     page=1
        ... )
        'https://www.csrc.gov.cn/searchList/059986f6f4834fe6ae61cb76bd9ef23b?_isAgg=false&_isJson=true&_pageSize=20&_template=index&_rangeTimeGte=&_channelName=&page=1'
    """
    path = api_path_template.format(channelid=channelid)

    query_params = {
        "_isAgg": "false",
        "_isJson": "true",
        "_pageSize": str(page_size),
        "_template": "index",
        "_rangeTimeGte": "",
        "_channelName": "",
        "page": str(page),
    }

    query_string = "&".join(f"{k}={v}" for k, v in query_params.items())

    return f"https://{host}{path}?{query_string}"


def build_detail_url(
    host: str, org_prefix: str, column_code: str, manuscript_id: str
) -> str:
    """构建 CSRC 详情页 URL

    Args:
        host: 主机名
        org_prefix: 组织前缀（如 szzyb, shzyb）
        column_code: 栏目代码（如 c101700）
        manuscript_id: 稿件 ID

    Returns:
        详情页完整 URL

    Examples:
        >>> build_detail_url("www.csrc.gov.cn", "szzyb", "c101700", "7652321")
        'https://www.csrc.gov.cn/szzyb/c101700/c7652321/content.shtml'
    """
    return f"https://{host}/{org_prefix}/{column_code}/c{manuscript_id}/content.shtml"
