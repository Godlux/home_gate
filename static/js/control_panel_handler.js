success = function () {
    // send user to control panel page
    console.log("Action Sucess")
};

trigger_button = function (button_id) {
    console.log("Button ID: " + button_id);

    $.ajax({
        type: "POST",
        url: "/api",
        data: JSON.stringify({ device: button_id, action: "toggle" } ),
        success: success(),
        contentType : 'application/json'
    })
};

$('.device_toggle_Button').click( function () {
    let device_id = $('.device_toggle_Button').attr('id');
    trigger_button(device_id);
});