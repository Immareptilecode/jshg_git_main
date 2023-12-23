var hide_success_share_capital=function(){
		$('#paysharecapitalform').removeClass('success')



	};

var hide_error_share_capital=function(){
		$('#paysharecapitalform').removeClass('error')



	};
var get_sharecapital=function(url){
$.get({
url,
success: function(data){
	var total = data[0].total;
	
	$('#members_totalsharecapital').html($.number(total));
},




})

};

var send_shareCapital=function(url, mem, url_get){


		var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

		$.ajax({
		    url: url,
		    type: "POST",
		    data: {csrfmiddlewaretoken: csrftoken, Amount:$("#sharecapital_amnt").val(), date:$("#sharecapital_date").val(), individual:mem},


		    success: function(e){
		     
		       
		     	$('#paysharecapitalform').addClass('success')
		     	setTimeout(hide_success_share_capital, 2000)
		     	get_sharecapital(url_get);
		        
		    },

		    error: function(f){
		    		console.log(f);
		    		$('#paysharecapitalform').addClass('error')
		    
		    	//console.log(f.responseJSON['detail'] === "Authentication credentials were not provided.");
		    }

		    });
	};

var Indi_sharecapital_ops = Indi_sharecapital_ops || (function(){
 
  var _args = {}; 

  return {

  	init: function(arguments){
  		_args =arguments;

  	},

  	send_sharecapital: function(){

  		send_shareCapital(_args[0], _args[1], _args[2]);
  	},

  	get_deductions: function(){

  		get_sharecapital(_args[2])
  	}


  };




}());