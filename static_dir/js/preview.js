// <<<<<<< HEAD

=======
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







// list item delete

// $("ul").on("click", "span", function(event){
// 	var result = confirm("Are you sure you want to delete the problem?");
// 	if (result) {
// 		$(this).parent().fadeOut(500,function(){
// 			var todoText = (this).attributes[0].value;
// 			$(this).val("");
// 			console.log(this)
// 			$(this).remove();

// 			$.ajax({
// 			    url: '/entry?id='+(this).attributes[0].value,
// 			    type: 'DELETE',
// 			    success: function(result) {
// 					// console.log(result, this);
// 			    }
// 			});
// 		});
	
// 	}
// 	event.stopPropagation();
	
// });
