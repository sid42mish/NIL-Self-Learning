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


console.log("connecteed");


// list item delete

$("ul").on("click", "span", function(event){
	
	$(this).parent().toggleClass('incorrect');
	
	event.stopPropagation();
	
});
