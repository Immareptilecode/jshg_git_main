$('#launch_payment_options').on('click', function(){


$("#choose_type").modal('show');


});



var get_payments=function(url){
		
		$.get(

			url,

			function(e){

				paystrg.set('payments', e)
				//console.log(e)

			},)



	};


var hide_error=function(){

		$('#payloanform').removeClass('error');
	};

var hide_success=function(){

		$('#payloanform').removeClass('success');
	};




var mark_rpd=function(url){
		
		$.get(

			url,

			function(e){

				//console.log(e);


			},)



	};
var send_loan_payment=function (url, loan){


		var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

	
		$.ajax({
		    url: url,
		    type: "POST",

		    data: {csrfmiddlewaretoken: csrftoken, Amount:parseInt($("#loan_amnt").val()), date_payment:$("#loan_DATE").val(), loan: loan },


		    success: function(e){
		        
		       	get_payments(url);
		       	
		     	$('#payloanform').addClass('success');
		     	setTimeout(hide_success, 3000);
		    
		        
		    },

		    error: function(f){
		    	console.log(f.responseJSON)
		    	if (f.responseJSON['detail'] === "Authentication credentials were not provided."){

		    		$('#payloanform').addClass('error')
		    	}
		    	else if (f.responseJSON['date_payment'] ){
		    		$('#errormessage').html("PLEASE ENTER THE DATE OF PAYMENT.");

		    		$('#payloanform').addClass('error');
		    		setTimeout(hide_error, 2000)
		    	}

		    
		    }

		    });
	};



var Group_loan_ops = Group_loan_ops || (function(){
    var _args = {}; // private

    return {
        init : function(Args) {
            _args = Args;
            // some other initialising
        },
        pay_loan : function() {
           
           	send_loan_payment(_args[0], _args[1]);

        },
    };
}());