
$(document).ready(fuction(){
	$('#btnSubmit').click(function(){
		var result = $('input[type="radio"]:checked');
		if(result.length>0)
		{
			$('#form').toggleClass("correct-ans");
		}
	})
})