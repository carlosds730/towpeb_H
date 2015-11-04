function ValidateCookie() {
    var strCookieName = "cookie-compliance";
    var strApprovedVal = "approved";

    var cookieVal = readCookie(strCookieName);

    var $displayMsg = $("#cookiesThing");


    if (cookieVal != strApprovedVal) {

        $displayMsg.fadeIn();
    } else if (!$displayMsg.is(':hidden')) {
        $displayMsg.fadeIn();
    }


    $('#cookieClose').click(function () {
        $displayMsg.fadeOut();
        createCookie(strCookieName, strApprovedVal, 1);
    });
}

//$(document).ready(function () {
//
//    var strCookieName = "cookie-compliance";
//    var strApprovedVal = "approved";
//
//    var cookieVal = readCookie(strCookieName);
//
//    var $displayMsg = $("#cookiesThing");
//
//
//    if (cookieVal != strApprovedVal) {
//
//        $displayMsg.fadeIn();
//    } else if (!$displayMsg.is(':hidden')) {
//        $displayMsg.fadeIn();
//    }
//
//
//    $('#cookieClose').click(function () {
//        $displayMsg.fadeOut();
//        createCookie(strCookieName, strApprovedVal, 1);
//    });
//});

//Cookie functions
function createCookie(name, value, days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        var expires = "; expires=" + date.toGMTString();
    }
    else var expires = "";
    document.cookie = name + "=" + value + expires + "; path=/";
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function eraseCookie(name) {
    createCookie(name, "", -1);
}