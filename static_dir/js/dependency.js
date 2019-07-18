// create new row
$(document).on("click", ".btn-add-row", function(){
    // clone row class element index 0
    console.log("adding new row")
    var row = $(".row").eq(0).clone().show();
    // append row clone to elemt-wraper
    $(".element-wrapper").append(row);
})

// remove row handle
$(document).on("click", ".btn-remove-row", function(){
    // get btn index first
 //   debugger;
    var result = confirm("Are you sure you want to remove?");
  	if(result){
		var i1=(this).attributes[1].value;
		var i2=(this).attributes[2].value;
		var todoText = (this).baseURI;
		console.log(this)
		console.log(todoText)
		$.ajax({
			headers: {
		        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
		    },
		    url: todoText,
		    data: {i1: i1, i2: i2},
		    type: 'DELETE',
		    error: function (request, error) {
		        console.log(arguments);
		        alert(" Can't do because: " + error);
		    },
		    success: function () {
		    	console.log("successful deletion")
   		//		window.location.reload(true);

		    }
		});
	
	}
//	event.stopPropagation();
})