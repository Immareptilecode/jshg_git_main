$('#choose_type').modal({blurring:true}).modal('attach events', '#launch_payment_options', 'show');


$("#download_receipt").accordion();
	$('#member_data').accordion();
	$(".ui.dropdown").dropdown();

	$('#menufinance #itemenufinance').tab();

	$('#debt_breakdown').accordion();

$('#payshares').modal({ blurring: true}).modal('attach events', '#launchpayshares', 'show');


	$('#paycharges').modal({
	    blurring: true
	  }).modal('attach events', '#paycharge', 'show');

	$('#payfines').modal({
	    blurring: true
	  }).modal('attach events', '#payfine', 'show');

	$("#addcharges").modal({blurring:true}).modal('attach events', '#add_charge', 'show');
	$("#addfines").modal({blurring:true}).modal('attach events', '#add_fine', 'show');



var get_charges_group=function(url){

	$.get(

		url,

		function(data){
			var total=0
			
			for (var i in data){
				total += parseInt(data[i].Amount)
				$("#table_body_charges").prepend('<tr id='+ i+2 +'><td>'+ data[i].details+'</td> <td>'+ data[i].Amount + '</td> <td> '+ data[i].Date +'</td> </tr>')
				$('#charges_choices').prepend('<div class="item" data-value="'+ data[i].pk +'"> '+ data[i].details+','+data[i].Amount+'</div>')

			}
			$('#charges_figure').html(total);
			//console.log(data)
			
		},






		)

}



var get_fines_group=function(url){

	$.get(

		url,

		function(data){
			var total=0
			console.log(data)
			for (var i in data){
				total+= data[i].Amount_due

				$("#table_body_fines").prepend('<tr><td>'+ data[i].Particulars+'</td> <td>'+ data[i].Amount_due + '</td> <td> '+ data[i].Date +'</td> </tr>')
				$('#fines_choices').prepend('<div class="item" data-value="'+ data[i].id +'"> '+ data[i].Particulars+','+data[i].Amount_due+'</div>')
			}
			
			$('#fines_figure').html(total);
		},






		)

}


var get_fines_group_after_payfine=function(url){

	$.get(

		url,

		function(data){
			var total=0
			$('#fines_choices').html(" ")
			$("#table_body_fines").html(" ")
			console.log(data)
			for (var i in data){
				total+= data[i].Amount_due

				$("#table_body_fines").prepend('<tr><td>'+ data[i].Particulars+'</td> <td>'+ data[i].Amount_due + '</td> <td> '+ data[i].Date +'</td> </tr>')
				$('#fines_choices').prepend('<div class="item" data-value="'+ data[i].id +'"> '+ data[i].Particulars+','+data[i].Amount_due+'</div>')
			}
			
			$('#fines_figure').html(total);
		},






		)

}


var get_charges_group_after_paycharge=function(url){

	$.get(

		url,

		function(data){
			var total=0
			$('#charges_choices').html(" ")
			$("#table_body_charges").html(" ")
			console.log(data)
			for (var i in data){
				total += parseInt(data[i].Amount)
				$("#table_body_charges").prepend('<tr id='+ i+2 +'><td>'+ data[i].details+'</td> <td>'+ data[i].Amount + '</td> <td> '+ data[i].Date +'</td> </tr>')
				$('#charges_choices').prepend('<div class="item" data-value="'+ data[i].pk +'"> '+ data[i].details+','+data[i].Amount+'</div>')
			}
			
			$('#charges_figure').html(total);
		},






		)

}






var get_fines_group_after_addfine=function(url){

	$.get(

		url,

		function(data){
			var total=0
			var the_added=data[data.length-1]
			//console.log()
			$('#fines_choices').prepend('<div class="item" data-value="'+ the_added.id +'"> '+ the_added.Particulars+','+the_added.Amount_due+'</div>')
			for (var i in data){
				total+= data[i].Amount_due

			
				
			}
			
			$('#fines_figure').html(total);
		},






		)

}



var get_charges_group_after_addcharge=function(url){

	$.get(

		url,

		function(data){
			var total=0
			var the_added_charge=data[data.length-1]
			console.log(the_added_charge);
			$('#charges_choices').prepend('<div class="item" data-value="'+ the_added_charge.pk +'"> '+ the_added_charge.details+','+the_added_charge.Amount+'</div>')
			for (var i in data){
				total += parseInt(data[i].Amount)
				
				

			}
			$('#charges_figure').html(parseInt(total));
			console.log(data)
			
		},






		)

}




// groups





var remove_success_charges=function(){

$('#addchargesform').removeClass('success');



}

var remove_error_charges=function(){

$('#addchargesform').removeClass('error');



}

var remove_error_fines=function(){

$('#addfinesform').removeClass('error');



}

var remove_success_fines=function(){

$('#addfinesform').removeClass('success');



}

var charge_acc=function(url, member_id){
	var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
		$.ajax({
			url:url,
			type: "POST",
			data:{csrfmiddlewaretoken: csrftoken, Amount_due:$('#charge_amount').val(), Date:$('#charge_date').val(), group:member_id, Particulars:$('#charge_parts').val()},


			success:function(message){
				$("#table_body_charges").prepend('<tr><td>'+ $('#charge_parts').val() +'</td> <td>'+ $('#charge_amount').val() + '</td> <td> '+ $('#charge_date').val() +'</td> </tr>')
				get_charges_group_after_addcharge(url)
				$('#addchargesform').addClass('success');
				setTimeout(remove_success_charges, 3000);
			
			},

			error:function(error){
				$('#addchargesform').addClass('error');
				console.log(error);
				setTimeout(remove_error_charges, 3000);
			}


			,



		});

}


var fine_acc=function(url, member_id){
	var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
		$.ajax({
			url:url,
			type: "POST",
			data:{csrfmiddlewaretoken: csrftoken, Amount_due:$('#fine_amount').val(), Date:$('#fine_date').val(), group:member_id, Particulars:$('#fine_parts').val()},


			success:function(message){
				$("#table_body_fines").prepend('<tr><td>'+$('#fine_parts').val()+'</td> <td>'+ $('#fine_amount').val() + '</td> <td> '+ $('#fine_date').val()+'</td> </tr>')
				get_fines_group_after_addfine(url)
			
				$('#addfinesform').addClass('success');
				setTimeout(remove_success_fines, 3000);

			},

			error:function(error){
				$('#addfinesform').addClass('error');
				console.log(error);
				setTimeout(remove_error_fines, 3000);
			}


			,



		});

}


var remove_success_paycharges=function(){

$('#paychargesform').removeClass('success');



}

var remove_error_paycharges=function(){

$('#paychargesform').removeClass('error');



}

var remove_error_payfines=function(){

$('#payfinesform').removeClass('error');



}

var remove_success_payfines=function(){

$('#payfinesform').removeClass('success');



}


var pay_charges=function(url, get_charges_url){
 

 var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
		$.ajax({
			url:url,
			type: "POST",
			data:{csrfmiddlewaretoken: csrftoken, Amount:$('#paycharges_amount').val(), date_payment:$('#paycharges_date').val(), charges:$('#paycharges_select').val()},


			success:function(message){
				get_charges_group_after_paycharge(get_charges_url)

				

				if (message === 'insufficient_funds'){
					$('#paycharges_error_message').html("The amount you have enterd is not enough to settle this fine.")
					$('#paychargesform').addClass('error');
					setTimeout(remove_error_paycharges, 4000);
				}
				else{
				$('#paychargesform').addClass('success');
				setTimeout(remove_success_paycharges, 3000);

				}
				

			

			},

			error:function(error){
				$('#paychargesform').addClass('error');
			
				setTimeout(remove_error_paycharges, 3000);

				
			}


			,



		});



}


var pay_fines=function(url, get_fines_url){
 

 var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
		$.ajax({
			url:url,
			type: "POST",
			data:{csrfmiddlewaretoken: csrftoken, Amount:$('#payfines_amount').val(), date_payment:$('#payfines_date').val(), fines:$('#payfines_select').val()},


			success:function(message){
				

				get_fines_group_after_payfine(get_fines_url)
				if (message === 'insufficient_funds'){
					$('#payfines_error_message').html("The amount you have enterd is not enough to settle this fine.")
					$('#payfinesform').addClass('error');
					setTimeout(remove_error_payfines, 4000);
				}
				else{
				$('#payfinesform').addClass('success');
				setTimeout(remove_success_payfines, 3000);

				}
				
			
				

			},

			error:function(error){
				$('#payfinesform').addClass('error');
				console.log(error)
				setTimeout(remove_error_payfines, 3000);
				
			}


			,



		});



}


var Group_debt_ops = Group_debt_ops || (function(){
    var _args = {}; // private

    return {
        init : function(Args) {
            _args = Args;
            // some other initialising
        },
        get_charges : function() {
           
            get_charges_group(_args[0]);
        },

        get_fines : function() {
           
            get_fines_group(_args[1]);
        },

        charge_account : function(){
        	charge_acc(_args[0], _args[2])
        },

        fine_account : function(){
        	fine_acc(_args[1], _args[2])
        },

        pay_fine : function(){
        	pay_fines(_args[3], _args[1])
        },

        pay_charge : function(){
        	pay_charges(_args[4], _args[0])
        },

    };
}
());