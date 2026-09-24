$(function(){
    $("#page_div").bindEvent({});
    table_ajax();
	var url = window.location.href;
	var codeNameLen=url.split('/').length;
	var codeName=url.split('/')[codeNameLen-2];
	var li = $('.sidebar li a');
	var zx2 = []
	for(var i = 0 ; i<li.length;i++){
		var zx =  $('.sidebar li a').eq(i).attr('href');
		var zx1=zx.split('/').length;
		zx2.push(zx.split('/')[zx1-2]);
			if(codeName === zx2[i]){
				$('.sidebar li').eq(i).addClass('active').siblings().removeClass('active');
		}
		if(zx.indexOf('https') >= 0 || zx.indexOf('http') >= 0){
			$('.sidebar li a').eq(i).attr('href',zx.split('?')[0]);
		}else if(zx.indexOf('zfxxgk_zdgk.shtml') > 0){
			var  _arr = zx.split('?');
			var _newArr = _arr.slice(0,2);
			$('.sidebar li a').eq(i).attr('href',_newArr.join('?'));
		}else if(zx.split('?').length > 2){
                        var  _arr = zx.split('?');
			var _newArr = _arr.slice(0,2);
			$('.sidebar li a').eq(i).attr('href',_newArr.join('?'));
                }
	}
	//请求面包屑
	rendChannel(codeName);
});
function GetQueryString(name) {
	var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)')
	var r = window.location.search.substr(1).match(reg)
	if(r != null) return decodeURI(r[2])
	return null
}
function table_page(totalHits) {
	var totalHits = parseInt(totalHits);
	
	var pageSize = parseInt($("#pageSize").val());
    var page = parseInt($("#page").val());
	var pageNum = Math.floor((totalHits + pageSize - 1) / pageSize);
	var options = {
		pageNum: pageNum,
		current: page,
		backfun: function(e) {
			console.log(e.current);
			$("#page").val(e.current);
			table_ajax();
		}
	}
	$("#page_div").createPage(options);
}

var channelid = GetQueryString('channelid')
function table_ajax() {
	$.ajax({
		url: '/searchList/'+channelid+'?_isAgg=false&_isJson=true&_pageSize='+$("#pageSize").val()+'&_template=index&_rangeTimeGte=&_channelName=&page=' + $("#page").val(),
		type: 'get',
		success: function(data) {
			table_page(data.data.total);
			table_each("list", ajax_success(data));
		},
		error: function(err) {
			console.log(err)
		}
	})
}

function ajax_success(json) {
	var list = [];
	var resutList = json.data.results;
	if(json.data.total <= 18) {
		$("#page_div").css("display", "none")
	} else {
		$("#page_div").css("display", "block")
	}
	$.each(resutList, function(name, val) {
		var myValues = val;
		var json = {
			"title": myValues.title,
			"url": myValues.url,
			"publishedTimeStr": val.publishedTimeStr
		}
		list.push(json);
	});
	return list;
}

function table_each(id, json) {
	var tab = $("#" + id);
	tab.empty();
	$.each(json, function(name, val) {
		var _li = '';
		_li += '<li><a href="' + val.url + '" target="_blank" title="' + val.title + '" >' +
			val.title + '</a><span class="date">' + (val.publishedTimeStr).substr(0, 10) + '</span></li>'
		tab.append(_li);
	});
	$('#list li').each(function(i){
		if((i + 1) % 6 == 0){
			$(this).css({
                'border-bottom' : '1px dashed #dbdbdb',
                'padding-bottom' : '25px',
                'margin-bottom' : '15px'
            });
		}
	})
}
//请求面包屑
function rendChannel(code) {
  $.ajax({
    url: '/getLocalList?channelCode=' + code,
    type: 'get',
    async: false,
    success: function(data){
      var _nav = '',_url = '',addUrl = '';
      if(data.code == '200'){
        _nav = '<img src="/csrc/xhtml/images/public/location.png" alt="">当前位置：<a href="/szzyb/index.shtml">首页</a> > '
		if(data.results.channelLevel.length == 1){
			_nav += '<a href="'+ data.results.channelLevel[0].staticUrl +'?channelid='+data.results.channelLevel[0].channelId+'">'+data.results.channelLevel[0].channelName+'</a>';
		}else{
			for(var i = 0; i < data.results.channelLevel.length; i++){
				//处理返回两个url
				if(data.results.channelLevel[i].staticUrl.indexOf(',') > 0){
					var _arr = data.results.channelLevel[i].staticUrl.split(',');
					for(var j = 0; j < _arr.length; j++){
					  if(_arr[j].indexOf('common_list') > 0){
						_url = _arr[j];
					  }
					}
				}else{
					_url = data.results.channelLevel[i].staticUrl;
				}
				if(i == 0){
					addUrl = data.results.channelLevel[i].staticUrl.indexOf('tz') > 0 ? data.results.channelLevel[i].staticUrl : (data.results.channelLevel[i].staticUrl + '?channelid=' + data.results.channelLevel[i].channelId)
					_nav += '<a href="'+ addUrl +'">'+data.results.channelLevel[i].channelName+'</a> > ';
				}else if(i != data.results.channelLevel.length -1){
					_nav += '<a href="'+ _url +'?channelid='+data.results.channelLevel[i].channelId+'">'+data.results.channelLevel[i].channelName+'</a> > ';
				}else{
					_nav += '<a href="'+ _url +'?channelid='+data.results.channelLevel[i].channelId+'">'+data.results.channelLevel[i].channelName+'</a>';
				}
			}
		}
      }
      $('.BreadcrumbNav').empty().html( _nav);
    },
    error: function(err){
      console.log(err);
    }
  })
};