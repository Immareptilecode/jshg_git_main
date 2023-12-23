
var get_groups_summary= function(url){
	 $.get(
	 	 url,

		function  (data) {
			$('#g_summary_search')
				.search({

					searchFields   : [
				      'membership_no'
				    ],

				    fields: {

				    
				    description: 'membership_no',
				    url: 'url',
				    title:'name'
				   },

				source: data,
				type: 'standard',

				    fullTextSearch: 'exact',
				    minCharacters: 3,

				    onSelect: function(result, response){
						$('#loansummary_group').modal('show');
						
}
				


			});
		},
		);
};






