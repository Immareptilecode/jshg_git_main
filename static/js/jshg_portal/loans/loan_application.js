

//the below get_groups_application  and get_members_application  are indeed the final steps of loan application

var get_groups_application= function(url){
	 $.get(
	 	 url,

		function  (data) {
			$('#gssearch')
				.search({

					searchFields   : [
				      'membership_no'
				    ],

				    fields: {

				    
				    description: 'membership_no',
				 
				    title:'name'
				   },

				source: data,
				type: 'standard',

				    fullTextSearch: 'exact',
				    minCharacters: 3,

				    onSelect: function(result, response){
						$('#loanform3').modal('show');
						$('#loanstep1').removeClass('completed');
						$('#loanstep2').removeClass('active');
				
						$('#loanstep1').addClass('active');
						$('#loanstep111').addClass('completed');
						$('#loanstep222').addClass('completed');
						$('#loanstep333').addClass('active');
						//$('#Group_applicant').prepend("<h2 class='ui dividing header'> Applicant Info</h2><div class='field'><label>Name</label><div class='two fields'>div class='field'><input name='' placeholder='First Name' type='text'></div><div class='field'><input name='' placeholder='Last Name' type='text'></div></div></div>  <h4 class='ui dividing header'>'+ result['name']+ ' '+'Group' +'</h4>");
						$('#groupname').val(result['name']);
						$('#Group_mno').val(result['membership_no']);
						$('#g_pk').val(result['pk']);
}
				


			});
		},
		);
};






var get_members_application= function(url){
	 $.get(
	 	 url,

		function  (data) {
					
					$('#mssearch')
					.search({

						searchFields   : [
					      'membership_no'
					    ],

					    fields: {

					    image: 'img',
					    description: 'membership_no',
					   	
					    title:'fname'
					   },

					source: data,
					type: 'standard',
					fullTextSearch: 'exact',
					minCharacters: 3,
					
					onSelect: function(result, response){
						$('#loanform2').modal('show');
						$('#loanstep1').removeClass('completed');
						$('#loanstep2').removeClass('active');
				
						$('#loanstep1').addClass('active');
						$('#loanstep11').addClass('completed');
						$('#loanstep22').addClass('completed');
						$('#loanstep33').addClass('active');
						console.log(response, result['lname'])
						
						
						$("#Individual_fname").val(result['fname']);
						$("#Individual_lname").val(result['lname']);
						$("#Individual_mno").val(result['membership_no']);
						$('#m_pk').val(result['pk']);
					}


					});

					

		},


		);
};

var hide_success=function(){

	$('#individual_loan_form').removeClass('success')
}

var hide_error=function(){

	$('#individual_loan_form').removeClass('error')
}
var hide_success_group=function(){

	$('#group_loan_form').removeClass('success')
}


var hide_error_group=function(){

	$('#group_loan_form').removeClass('error')
}


//post p



	function send_app_individual( url){

		var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
		$.ajax({
		    url: url,
		    type: "POST",
		    data: {csrfmiddlewaretoken: csrftoken, Amount:$("#individual_loan_amount").val(), Date_disbursment:$("#individual_loan_date").val(), Borrower:$("#m_pk").val(), 'gurantor': $("#Individual_gurantors").val(), installments:$("#individual_loan_period").val()},


		    success: function(e){
		        if (e === "UNPAID_LOAN"){

		        	$('#individual_loan_form').addClass('error')
		        	setTimeout(hide_error, 2000)
		        }
		        else if (e === 'success'){
		        	$('#individual_loan_form').addClass('success')
		        	setTimeout(hide_success, 2000)

		        }
		        
		        
		    },

		    error: function(f){
		    	console.log(f.responseJSON );
		    	if (f.responseJSON['detail'] === "Authentication credentials were not provided."){

		    	
		    	}
		    	//console.log(f.responseJSON['detail'] === "Authentication credentials were not provided.");
		    }

		    });
	};



function send_app_group( url){

		var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

		$.ajax({
		    url: url,
		    type: "POST",
		    data: {csrfmiddlewaretoken: csrftoken, Amount:$("#group_loan_amount").val(), Date_disbursment:$("#group_date_disbursment").val(), Borrower:$("#g_pk").val(), 'gurantor': $("#group_gurantors").val(), installments:$("#group_loan_period").val()},


		    success: function(e){
		         if (e === "UNPAID_LOAN"){

		        	$('#group_loan_form').addClass('error');
		        	setTimeout(hide_error_group, 3000);
		        	console.log(e);
		        }
		          else if (e === 'success'){
		        	$('#group_loan_form').addClass('success');
		        	setTimeout(hide_success_group, 3000);
		        }
		        
		        
		        
		    },

		    error: function(f){

		    	console.log(f );
		    	if (f.responseJSON['detail'] === "Authentication credentials were not provided."){
		    		$('#group_loan_form').html('The system may have logged you out.Please reload the page to refresh login details. ');
		    		$('#group_loan_form').addClass('error');
		    	}
		    	//console.log(f.responseJSON['detail'] === "Authentication credentials were not provided.");
		    }

		    });
	};



