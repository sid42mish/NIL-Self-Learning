// <<<<<<< HEAD

// =======
// correct answer
// >>>>>>> 25b0026bb6bb5287ca3322f915f9f6a7be3a244f
// $(document).ready(fuction(){
// 	$('#btnSubmit').click(function(){
// 		var result = $('input[type="radio"]:checked');
// 		if(result.length>0)
// 		{
// 			$('#form').toggleClass("correct-ans");
// 		}
// 	})
// })


// console.log("connecteed");


// list item delete

$("ul").one("click", "li", function(event){
	var title=this.attributes[2].value
	var redir=this.baseURI
	var select=this.attributes[1].value
	var x=this
	var righ;
	// console.log(redir)
	$.ajax({
		url: redir,
	    type: "POST",
	    data: {title: title, select: select},
	    error: function (request, error) {
	        // console.log(arguments);
	        alert(" Can't do because: " + error);
	    },
	    success: function(result) {
	    	// console.log("Hurray!!!!!!",result)
	    	// console.log(x)
	    	// console.log(result.right ,result.submi)
	    	if (result.right==result.submi){
	    		// console.log("correct")
	    		$(x).toggleClass('correct');
	    	}
	    	else{
	    		// console.log("incorrect")
	    		$(x).toggleClass('incorrect');	
	   		}
					
		}
	});
	
	//explanation
	$(".formul").css("display", "block");

	//functionality closes due to "one"


	event.stopPropagation();
	
});


