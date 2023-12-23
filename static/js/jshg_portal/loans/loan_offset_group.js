$('#loan_offset_group').modal({blurring:true}).modal('attach events', '#launch_offset_group', 'show');

//post 


var hide_error_offset_group=function(){

		$('#offsetloanform_group').removeClass('error');
	};

var hide_success_offset_group=function(){

		$('#offsetloanform_group').removeClass('success');
	};





var offset_loan_group= function(url, subject_loan){
	var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
	$.ajax({
			url:url,
			type:"POST",
			data:{csrfmiddlewaretoken: csrftoken, loan: subject_loan, balance_amount:$('#offset_amount_group').val(), date:$('#offset_date_group').val()},

			success:function(success){
				if (success === 'FAILED Cause Amount Not Same'){

				$("#errormessage_offset_group").html('The Amount you entered was not enough to offset the loan balance! Tip: BE SURE TO INCLUDE ANY DECIMAL FIGURES IN THE AMOUNT.')
				$('#offsetloanform_group').addClass('error');
				setTimeout(hide_error_offset_group, 5000);

				}
				else if(success === 'FAILED Cause Shares Not Enough'){
				$("#errormessage_offset_group").html('This Group does not have enough shares to offset loan!')
				$('#offsetloanform_group').addClass('error');
				setTimeout(hide_error_offset_group, 5000);

				}
				else if (success === 'success'){
				$("#success_message_offset_group").html('Loan Offset Operation Copmpleted!')
				$('#offsetloanform_group').addClass('success');
				setTimeout(hide_success_offset_group, 5000);

				}

				else if (success === 'FAILED'){
					$("#success_message").val('Please Contact the developer. Some unexpected error occured.')


				}
				

			},


			error:function(error){

				console.log(error);

			},

		});
}


var Group_offset_ops = Group_offset_ops || (function(){


	var _args = {};

 return {
        init : function(Args) {
            _args = Args;
            // some other initialising
        },
        send_offset_request: function(){

        	offset_loan_group(_args[0], _args[1],)
        },

    };





}
());