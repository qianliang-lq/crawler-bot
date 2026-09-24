# csrc-shzyb-3fde NOTES

- Same `CsrcSearchListAdapter` as SZ; params only: channelid=3fdeb6b6…, org_prefix=shzyb, column_code=c101682
- Shell sample `csrc_sh.html`: SiteName=上海专员办, ColumnName=通知公告, `#list` empty (len=0)
- Shares `common_list.js` AJAX pattern: `/searchList/{channelid}?_isJson=true&...`
- Live JSON sample for SH not re-fetched this session (WAF/TLS); morphology parity + identical 302 behavior on prefixed searchList proves same family
- Expected detail pattern: `https://www.csrc.gov.cn/shzyb/c101682/c{manuscriptId}/content.shtml`
