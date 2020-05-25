success = function (data) {
    // send user to control panel page
	if (data == "true") {
		window.location.reload();
	}
};

do_login = function () {
    login = $('#login').val();
    password = $('#password').val();

    $.ajax({
        type: "POST",
        url: "/do_login",
        data: JSON.stringify({ login: login, password: password } ),
        success: function (data) {
			success(data);
		},
        contentType : 'application/json'
    })
};

$('#send_button').click(do_login);