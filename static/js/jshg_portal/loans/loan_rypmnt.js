$('#group_loan_amount').on('change', function(){
var valu=parseInt($('#group_loan_amount').val());

var va=new Number(valu);

//console.log(typeof(parseInt(valu)));
if ( valu <= 101000){
	$("#group_loan_period").val("12");
	
}
else if (va <= 201000  && va >= 101000){
	$("#group_loan_period").val('18');
}


else if (va >= 201000 && va <=301000){
	$("#group_loan_period").val('24');
}

else if (va >= 301000 && va <= 500000){
	$("#group_loan_period").val('36');
}

else if (va >= 501000 && va <= 1000000){
	$("#group_loan_period").val('48');
}
else {
	$("#group_loan_period").val('0');
}


//end of event callback function



});


$('#individual_loan_amount').on('change', function(){
var valu=parseInt($('#individual_loan_amount').val());

var va=new Number(valu);
console.log(va);
//console.log(typeof(parseInt(valu)));
if ( valu <= 101000){
	$("#individual_loan_period").val("12");
	
}
else if (va <= 201000  && va >= 101000){
	$("#individual_loan_period").val('18');
}


else if (va >= 201000 && va <=301000){
	$("#individual_loan_period").val('24');
}

else if (va >= 301000 && va <= 500000){
	$("#individual_loan_period").val('36');
}
else {
	$("#individual_loan_period").val('0');
}


//end of event callback function



});



$('#launch_payment_options').on('click', function(){


$("#choose_type").modal('show');


});



var get_payments=function(url){
		
		$.get(

			url,

			function(e){

				paystr.set('payments', e)
				console.log(e)

			},)



	};


var hide_error=function(){

		$('#paysharesform').removeClass('error');
	};

	var hide_success=function(){

		$('#paysharesform').removeClass('success');
	};




var mark_rpd=function(url){
		
		$.get(

			url,

			function(e){

				console.log(e);


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



var Indi_loan_ops = Indi_loan_ops || (function(){
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
