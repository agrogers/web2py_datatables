
// -------------------------------------------------------------------------------------------------------
//                                Functionality for the image picker
// -------------------------------------------------------------------------------------------------------

$( "#image-picker-form" ).submit(function( event ) { 
    event.preventDefault();
    SubmitMediaSearch();
});

function SubmitMediaSearch() {

    FormElement = "image-picker-form";
    // var formElem = $(`#${FormElement}`);
    // var formData = new FormData(formElem[0]);

    var form = $("#image-picker-form");
    var url =  "/smartdeck/maintenance/ImagePicker/"
    data = form.serializeArray(); // serializes the form's elements.

    $.ajax({    
        // contentType: 'application/json; charset=utf-8',
        // dataType: 'json', // The datatype of the result. json for objects, remove for HTML
        type: 'POST',
        async: false,
        timeout: 20000,
        url: url,
        data: data,
        success: function (result) { 
            $("#image-list").html(result);  
        },
        failure: function (response) {          
            alert('fail');
        }
    });        
}

function MediaItem_OnClick(MediaID) {


    CurrentRecordID = Current_id
    CurrentTableName = CurrentTableName.toLowerCase();
    if (CurrentRecordID == null) { // Possible that this is a new record so there is no ID yet.
        var url =  `/smartdeck/${CurrentTableName}/put?MediaID=${MediaID}`;
    } else {
        var url =  `/smartdeck/${CurrentTableName}/put/${CurrentRecordID}?MediaID=${MediaID}`;
    }
    $.ajax({    
        type: 'POST', async: false, timeout: 20000,
        dataType: 'json', // The datatype of the result. json for objects, remove for HTML
        url: url,
        // data: data,
        success: function (result) {
            if (result.Success) {
                // alert('It worked, do soemthing');
                if (CurrentTableName=='stockitem') {
                    $("#StockItem_MediaID").val(MediaID);
                    $("#MediaIcon").attr('src',Get_URL('default','image_download', result.Icon));
                    $("#MediaDescription").html(result.Description);
                    if ($("#StockItem_Description").val()==''){$("#StockItem_Description").val(result.Description)}
                    $("#image-selector-dialog").modal('hide');
                } else {
                    alert("Don't know what to do with that table.")
                }
            } else {
                alert(`It failed: ${result.Message}`);
            }
        },
        failure: function (response) {          
            alert('fail');
        }
    });   

}
