function utilizouHoraExtra(id){
	token = document.getElementByName('csrfmiddlewaretoken')[0].value;
	console.log(id);
	$.ajax({
		type: 'POST',
		url: '/horas-extras/utilizou-hora-extra/' + id + '/',
		data: {
			csrfmiddlewaretoken: token
		},
		sucess: function(result){
			console.log(result);
			$("#mensagem").text(result.mensagem);
			$("#horas_atualizadas").text(result.horas);
		}
	});
}