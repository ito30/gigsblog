function searchPost() {
	$("#search").keyup(function(){
        var formData = $("#search").serializeArray();
		ajaxGet('/ajax_post_search', formData, function(data){
            //onSuccess
            $('div#content').html(data);
            // console.log(data)
        });
    });
}