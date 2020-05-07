success = function () {
  // send user to control panel page
};

do_login = function () {
    login = $('#login').val();
    password = $('#password').val();

    $.ajax({
        type: "POST",
        url: "/do_login",
        data: JSON.stringify({ login: login, password: password } ),
        success: null,
        contentType : 'application/json'
    })
};

$('#send_button').click(do_login);