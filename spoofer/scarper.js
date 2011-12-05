var x = new Array();
for(var i = 0;i<$(".site-listing").length;i++){
	x[i] = new Object();
	if ( $(".site-listing:eq("+i+")>.desc-container>h2>a")[0] != null){
		x[i].title = $(".site-listing:eq("+i+")>.desc-container>h2>a")[0].innerText
	}
	if ( $(".site-listing:eq("+i+")>.desc-container>span")[0] != null){
		x[i].url = $(".site-listing:eq("+i+")>.desc-container>span")[0].innerText
	}
}
JSON.stringify(x)