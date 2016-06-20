var page_num=1;
var loading=false;
var select_condition = new Array();
var command = "";
var min_score = "1000000";
$.getData = function() {
  page_num += 1;
  $.ajax({
    url: "get_more_people",
    type: "POST",
    contentType: "application/json; charset=utf-8",
    dataType: "json",
	data: '{"min_score":"' +min_score +'", "page_num": "'+page_num+'", "condition":"'+select_condition+'", "command":"'+command+'"}',
    success: function(data, textStatus, xhr) {
      	console.log(data)
      	min_score = data.min_score
	    $(".people_list").append(data.html);
	    loading = false;

    },
    error: function(xmlHttpRequest, textStatus, errorThrown) {
      loading = true;
      console.log(errorThrown.toString());
    }
  });
};


$(window).scroll(function() {
  // When scroll at bottom, invoked getData() function.
  if ($(window).scrollTop() + $(window).height() > $(document).height()-500 ) {
    if (!loading) {
      loading = true;   // Blocks other loading data again.
      console.log("start scroll")
      $.getData();
    }
  }
});

$(function() 
{   
	$("#search-form").keyup(function(e)
	{   
		if(e.which === 13) 
		{             
			start_search($("#search-form").val());
		}     
	});


});

$(function() 
{   
	$("#img-search").click(function()
	{
		start_search($("#search-form").val() );
	});
});

function bind_label_click(){
  $('[name=label-click]').each( function(){
	  	 $(this).on('click',function(){
			  	var command = $(this).attr("value")
			  	$("#search-form").val( command )
			    start_search(command)
		  	});
  }); 

}

$(document).ready( function(){ bind_label_click() } );

function start_search(command)
{	
	$("#search-form").val( command )
	var result = new Array();
    $("[name = chkItem]:checkbox").each(function () {
        if ($(this).is(":checked")) { 
            result.push($(this).attr("value"));
        }
    });
	page_num = 1;
	min_score=10000000;
	select_condition = result;
	

	$.ajax({
	  url: "get_more_people",
	  type: "POST",
	  contentType: "application/json; charset=utf-8",
	  dataType: "json",
	  data: '{"min_score":"' +min_score +'", "page_num": "'+page_num+'", "condition":"'+select_condition+'", "command":"'+command+'"}',
	  success: function(data, textStatus, xhr) {
	  	console.log(data)

	  	window.scrollTo(0,0);
	    $(".people_list").html(data.html);
	    $(".fields_list").html(data.fields_html);
	    bind_label_click()
	    min_score = data.min_score
	    loading = false;
	    },
	  error: function(xmlHttpRequest, textStatus, errorThrown) {
	    loading = true;
	    console.log(errorThrown.toString());
	    }
	  });      
}

function person_detail(id)
{
	alert(id);
	location.href = "detail/"+id;
}

