<<<<<<< HEAD

=======
// correct answer
>>>>>>> 25b0026bb6bb5287ca3322f915f9f6a7be3a244f
$(document).ready(fuction(){
	$('#btnSubmit').click(function(){
		var result = $('input[type="radio"]:checked');
		if(result.length>0)
		{
			$('#form').toggleClass("correct-ans");
		}
	})
})


//randomize
var ul = document.querySelector('ul');
for (var i = ul.children.length; i >= 0; i--) {
    ul.appendChild(ul.children[Math.random() * i | 0]);
}