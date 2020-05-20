var buttons_action = {};

send_power_trigger_request_success_funciton = function (button_id) {
    // send user to control panel page
    console.log("Action Sucess")

	// // set actual info on button and description after success
	// let key = button_id;
	// if (buttons_action[key] === "turn_on") {buttons_action[key] = "turn_off"; $('#device_'+key+'_info').text("Устройство включено."); $('#device_'+key+'_button').prop('value', "Выключить");}
	// if (buttons_action[key] === "turn_off") {buttons_action[key] = "turn_on"; $('#device_'+key+'_info').text("Устройство выключено."); $('#device_'+key+'_button').prop('value', "Включить");}
};

send_power_trigger_request = function (button_id) {
    console.log("Button ID: " + button_id);
    //let device_action = buttons_action[button_id];
    let device_action = "power_toggle";

    $.ajax({
        type: "POST",
        url: "/api",
        data: JSON.stringify({ device: button_id, action: device_action } ),
        success: send_power_trigger_request_success_funciton(button_id),
        contentType : 'application/json'
    })
};

update_device_info_success_funciton = function (data) {
    // send user to control panel page
    console.log("Update action sucess function. Received data: " + data);
	$.each(data, function (key, value) {
		let text = "";

		if (value === "motion") {
			text = "Зафиксировано движение."
		}
		if (value === "no motion") {
			text = "Нет движения."
		}
		if (value === "On") {
			text = "Устройство включено.";
			$('#device_'+key+'_button').prop('value', "Выключить");
			buttons_action[key] = "turn_off";
		}
		if (value === "Off") {
			text = "Устройство выключено.";
			$('#device_'+key+'_button').prop('value', "Включить");
			buttons_action[key] = "turn_on";
		}
        $('#device_'+key+'_info').text(text)
	})
};

update_device_info = function () {
    console.log("updating... ");

    $.ajax({
        type: "POST",
		dataType: "json",
        url: "/get_devices_info",
        data: JSON.stringify({ action: "update_device_info" } ),
        success: function(data) {
           update_device_info_success_funciton(data)
        },
        contentType : 'application/json'
    });

};

$('.device_power_toggle_Button').click( function () {
    let device_id = $('.device_power_toggle_Button').attr('id').replace('device_', '').replace('_button', '');
    send_power_trigger_request(device_id);
});

$(document).ready(function() {
	update_device_info();
	let update_timer = setInterval(update_device_info, 1500);
});