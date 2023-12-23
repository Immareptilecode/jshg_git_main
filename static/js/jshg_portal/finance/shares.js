var hide_success=function(){
		$('#paysharesform').removeClass('success')



	};

	//get 
	var get_shares=function(url){
		$.get({
			url,
		success: function(data){
			total_shares=0
			
		

	
			var label_share=$("#members_totalshares").html($.number(data[0]))

			//	console.log(label_share)

		},

	

	
		});


	};

	//post
var send_shares=function(url, mem, url_get){


		var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

		$.ajax({
		    url: url,
		    type: "POST",
		    data: {csrfmiddlewaretoken: csrftoken, Amount:$("#amnt").val(), date_payment:$("#DATE").val(), member:mem},


		    success: function(e){
		        var sharesmodal=document.getElementById("payshares")
		       
		     	$('#paysharesform').addClass('success')
		     	setTimeout(hide_success, 1000)
		     	get_shares(url_get);
		        
		    },

		    error: function(f){
		    	if (f.responseJSON['detail'] === "Authentication credentials were not provided."){

		    		$('#paysharesform').addClass('error')
		    	}
		    	//console.log(f.responseJSON['detail'] === "Authentication credentials were not provided.");
		    }

		    });
	};


var Indi_share_ops = Indi_share_ops || (function(){
    var _args = {}; // private

    return {
        init : function(Args) {
            _args = Args;
            // some other initialising
        },
        get_shares : function() {
           
            get_shares(_args[2]);
        },

        give_me_shares : function(){
        	send_shares(_args[0], _args[1], _args[2])
        },
    };
}
());