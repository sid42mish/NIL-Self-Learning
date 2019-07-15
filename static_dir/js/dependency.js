// create new row
$(document).on("click", ".btn-add-row", function(){
    // clone row class element index 0
    console.log("adding new row")
    var row = $(".row").eq(0).clone().show();
    console.log(row);
    // append row clone to elemt-wraper
    $(".element-wrapper").append(row);
})

// remove row handle
$(document).on("click", ".btn-remove-row", function(){
    // get btn index first
    var index = $(".btn-remove-row").index(this);
    // do remove row
    $(".row").eq(index).remove();
})