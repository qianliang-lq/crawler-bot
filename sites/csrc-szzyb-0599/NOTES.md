# csrc-szzyb-0599 NOTES

- Family: `csrc_search_list`（与沪办同 Adapter，仅换 channelid / org_prefix / column_code）
- Shell: `csrc_sz.html` HTTP 200 historically; `#list` inner empty
- List JSON sample: `reg-crawl-samples/csrc_searchList_sample.json` — `data.total=56`, channelName=通知公告
- Detail URL pattern confirmed from results[].url + manuscriptId
- 2026-09-24 live re-probe from shared box egress: TLS EOF or WAF `acw_tc`→302 homepage — production should use stable/intranet egress or headed HAR
