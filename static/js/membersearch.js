$('#msearch')
.search({
apiSettings:{
	url:'//api.github.com/search/repositories?q={query}'
},
fields: {
      results : 'items',
      title   : 'name',
      url     : 'html_url'
    },
    minCharacters : 3





});