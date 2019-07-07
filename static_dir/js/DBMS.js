// Check Off Specific Todos By Clicking
// $(".dropbtn").on("click", function(){
// 	$("#formul").toggleClass("dropdown");
// });

$(".dropbtn").click( function() {
    $("#formul").css("display", "block");
});

$("ul").on("click", "span", function(event){
	var result = confirm("Are you sure you want to delete?");
	if (result) {
		$(this).parent().fadeOut(500,function(){
			var todoText = (this).attributes[1].value;
			var todoT = (this).attributes[2].value;
			console.log(this)
			console.log(todoText)
			console.log(todoT)
			$(this).remove();

			$.ajax({
			    url: '/course/'+todoT+'?id='+(this).attributes[1].value,
			    type: 'DELETE',
			    success: function(result) {
					// console.log(result, this);
			    }
			});
		});
	
		event.stopPropagation();
	}
});
