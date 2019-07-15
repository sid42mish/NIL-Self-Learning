$('label').click(function() {
    console.log(this)
    if(this.attributes[0].value=="Fastlearning"){
		const Url='/course/{{name}}/preview-course?id=0'
  		$post(Url,fuction(){

	    });
    }	
	else{
		const Url='/course/{{name}}/preview-course?id=0'
		$post(Url,fuction(){

		});
	}       
})




$(document).ready(fuction(){
	$('#btnSubmit').click(function(){
		var result = $('input[type="radio"]:checked');
		if(result.length>0)
		{
			$('#form').toggleClass("correct-ans");
		}
	})
})