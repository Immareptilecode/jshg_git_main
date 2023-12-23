$('#loan_offset').modal({blurring:true}).modal('attach events', '#launch_offset', 'show');

//post 


var hide_error_offset=function(){

		$('#offsetloanform').removeClass('error');
	};

var hide_success_offset=function(){

		$('#offsetloanform').removeClass('success');
	};





var offset_loan_individual= function(url, subject_loan){
	var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
	$.ajax({
			url:url,
			type:"POST",
			data:{csrfmiddlewaretoken: csrftoken, loan: subject_loan, balance_amount:$('#offset_amount').val(), date:$('#offset_date').val()},

			success:function(success){
				if (success === 'FAILED Cause Amount Not Same'){

				$("#errormessage_offset").html('The Amount you entered was not enough to offset the loan balance! Tip: BE SURE TO INCLUDE ANY DECIMAL FIGURES IN THE AMOUNT.')
				$('#offsetloanform').addClass('error');
				setTimeout(hide_error_offset, 5000);

				}
				else if(success === 'FAILED Cause Shares Not Enough'){
				$("#errormessage_offset").html('This member does not have enough shares to offset loan!')
				$('#offsetloanform').addClass('error');
				setTimeout(hide_error_offset, 5000);

				}
				else if (success === 'success'){
				$("#success_message_offset").html('Loan Offset Operation Copmpleted!')
				$('#offsetloanform').addClass('success');
				setTimeout(hide_success_offset, 5000);

				}

				else if (success === 'FAILED'){
					$("#success_message_offset").val('Please Contact the developer. Some unexpected error occured.')


				}
				

			},


			error:function(error){

				console.log(error);

			},

		});
}


var Indi_offset_ops = Indi_offset_ops || (function(){


	var _args = {};

 return {
        init : function(Args) {
            _args = Args;
            // some other initialising
        },
        send_offset_request: function(){

        	offset_loan_individual(_args[0], _args[1],)
        },

    };





}
());