$('#myform').submit(function(){
	var result = new Array();
    $("[name = chkItem]:checkbox").each(function () {
        if ($(this).is(":checked")) {
            result.push($(this).attr("value"));

    		console.log($(this).attr("value"));
        }
    });
    alert(result.join(","));
	page_num = 1;

	$.ajax({
	  url: "get_more_people",
	  type: "POST",
	  contentType: "application/json; charset=utf-8",
	  dataType: "json",
	  data: "{groupNumber:" + page_num + "}",
	  success: function(data, textStatus, xhr) {
	  	console.log(data)
	    $(".people_list").html(data.html);
	    loading = false;
	    },
	  error: function(xmlHttpRequest, textStatus, errorThrown) {
	    loading = false;
	    console.log(errorThrown.toString());
	    }
	  });
	return true;
});
