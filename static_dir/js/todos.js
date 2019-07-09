// Check Off Specific Todos By Clicking
// $("ul").on("click", "li", function(){
// 	$(this).toggleClass("completed");
// });

//Click on X to delete Todo

$("ul").on("click", "span", function(event){
	var result = confirm("Are you sure you want to delete the problem?");
	if (result) {
		$(this).parent().fadeOut(500,function(){
			var todoText = (this).attributes[0].value;
			$(this).val("");
			console.log(this)
			$(this).remove();

			$.ajax({
			    url: '/entry?id='+(this).attributes[0].value,
			    type: 'DELETE',
			    success: function(result) {
					// console.log(result, this);
			    }
			});
		});
	
	}
	event.stopPropagation();
	
});

$("input[type='text']").keypress(function(event){
	if(event.which === 13){
		//grabbing new todo text from input
		var todoText = $(this).val();
		$(this).val("");
		console.log(todoText)
		$.ajax({
		    url: '/entry?id='+todoText,
		    type: 'POST',
		    success: function(result) {
				// console.log(result, this);
				console.log('maal', result);
				$("ul.topiclist").after("<li><span><i class='fa fa-trash'></i></span><a class =\"main_item\" href=\"/course/" + result.course_name + "\"> " + result.course_name + "</a></li>")
				window.location.reload(true);
		    }
		});
	}
});

$("#toggle-form").click(function(){
	$("input[type='text']").fadeToggle();
});