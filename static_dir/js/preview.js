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