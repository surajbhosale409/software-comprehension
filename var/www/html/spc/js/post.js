function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ') {
                    c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                    return c.substring(name.length, c.length);
            }
    }
    return "";
}

function reply(my_id) {
    if(getCookie("email") == "")
    {
        alert("please login.");
        return;
    }
    console.log(my_id);

    var text_box_id = "#"+my_id+"_textarea_reply_div"
    $(text_box_id).show();
    $("#"+my_id).hide(); 
}


function edit(my_id) {
    if(getCookie("email") == "")
    {
        alert("please login.");
        return;
    }
    console.log(my_id); 
    var text_box_id = "#"+my_id+"_textarea_reply_div"    
    $(text_box_id).show();
    $("#"+my_id).hide(); 
}

function submit_reply(my_id) {

    console.log(my_id);
    var comment = $("#"+my_id+"_textarea_reply").val();

    var requestt = {}
    requestt["email"] =  getCookie("email");
    requestt["comment_id"] = my_id;
    requestt["new_comment"] = comment;
    requestt["request"] = "new_comment";

    $.post(location.protocol+"//"+window.location.hostname+"/forum",
    JSON.stringify(requestt),function(response,status){
        alert(response);
    });

    window.location.reload();
    console.log(comment);
}

function edit(my_id)
{
    console.log(my_id);
    var comment = $("#"+my_id+"_textarea_reply").val();

    var requestt = {}
    requestt["email"] =  getCookie("email");
    requestt["comment_id"] = my_id;
    requestt["new_comment"] = comment;
    requestt["request"] = "edit_comment";

    $.post(location.protocol+"//"+window.location.hostname+"/forum",
    JSON.stringify(requestt),function(response,status){
        alert(response);
    });
    
    window.location.reload();
    console.log(comment);
}
var app = angular.module('myApp', []);
app.controller('myCtrl', function($scope,$http,$interval,$q,$location) {
    
    $scope.detailed_post_view_div = function(code) {console.log(code);document.getElementById("post_and_comments_div").innerHTML = code;}
    
    $scope.getQueryVariable = function(variable){var query = window.location.search.substring(1);var vars = query.split('&');for (var i = 0; i < vars.length; i++) {var pair = vars[i].split('=');if (decodeURIComponent(pair[0]) == variable) {return decodeURIComponent(pair[1]);}}console.log('Query variable %s not found', variable);}



    $scope.is_object = function (something) {return typeof (something) == 'object' ? true : false;};
    
    var id = $scope.getQueryVariable("id");
    var data = {}
    data["request"] = "get_comments"
    data["id"] = id;
    var url = location.protocol+"//"+window.location.hostname+"/forum",config='application/x-www-form-urlencoded';
    $http.post(url, JSON.stringify(data), config).then(function (response) {
        $scope.detailed_post_view_div(response["data"]);
        //$scope.all_comments = response["data"];
        console.log(response["data"]);   
    }, function (response) {
   	        console.log("server error");
    });
    
    $scope.detailed_post_view_div("<h1>hellscso</h1>")
    // interval for getting all posts every second
    //$interval(function(){var data = {};data["request"] = "get_topics";var url = location.protocol+"//"+window.location.hostname+"/forum",config='application/x-www-form-urlencoded';$http.post(url, JSON.stringify(data), config).then(function (response){$scope.topics = response["data"];});}, 1000);

    $scope.logged_user = "Guest";
    
    $scope.ip = "hello";
    var x;
    $scope.setCookie = function(cname, cvalue, exdays) {var d = new Date();d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));var expires = "expires="+d.toUTCString();document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";}
    $scope.getCookie = function(cname){var name = cname + "=";var ca = document.cookie.split(';');for(var i = 0; i < ca.length; i++) {var c = ca[i];while (c.charAt(0) == ' ') {c = c.substring(1);}if (c.indexOf(name) == 0) {return c.substring(name.length, c.length);}}return "";}
    $scope.get_private_ip_address = function(){window.RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;/*compatibility for Firefox and chrome*/ var pc = new RTCPeerConnection({iceServers:[]}), noop = function(){};pc.createDataChannel('');/*create a bogus data channel*/pc.createOffer(pc.setLocalDescription.bind(pc), noop);/* create offer and set local description*/ pc.onicecandidate = function(ice){if (ice && ice.candidate && ice.candidate.candidate){var localIP = /([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/.exec(ice.candidate.candidate)[1];$scope.ip = localIP;console.log('local IP: ', localIP);x = localIP;pc.onicecandidate = noop;}};}
    // checking if coockies are set
    if($scope.getCookie("email")!=""){$scope.logged_user = $scope.getCookie("email");$scope.hide_login_and_signup = true;}


    $scope.login = function() {
        var email = $scope.email;
        var password = $scope.password;
        var data = {}
        data["email"] = email;
        data["password"] = password;
        data["request"] = "login";
        var url = location.protocol+"//"+window.location.hostname+"/forum",config='application/x-www-form-urlencoded';
        $http.post(url, JSON.stringify(data), config).then(function (response) {
            // This function handles success
            console.log(response["data"]);
            if(response["data"]=="True"){
                $scope.hide_login_and_signup = true;
                $scope.setCookie("email",email,1);
                $scope.logged_user = email;
                // set coockies here
            }
            else{
                alert("Invalid Password");
            }
        }, function (response) {
   	        console.log("server error");
    });
   }

   $scope.signup = function() {
        var email = $scope.email;
        var password = $scope.password;
        var cnf_password = $scope.cnf_password;
        var username = $scope.username;
        
        var data = {}
        data["email"] = email;
        data["password"] = password;
        data["username"] = username;
        data["cnf_password"] = cnf_password;

        data["request"] = "signup";
        
        var url = location.protocol+"//"+window.location.hostname+"/forum",config='application/x-www-form-urlencoded';
        $http.post(url, JSON.stringify(data), config).then(function (response) {
        // This function handles success
            if(response["data"]=="True"){
                $scope.hide_login_and_signup = true;
                // set coockies here
            }
            else{
                alert(response["data"]);
            }
        }, function (response) {
           console.log("server error");
        });
   }
   
   $scope.reply = function() {
       console.log("kdjabvkisdibvi");
    }

   $scope.get_new_post = function(){
        var data = {}
        data["new_post"] = $scope.new_post_text;
        data["email"] = $scope.getCookie("email");
        data["request"] = "new_topic";
        var url = location.protocol+"//"+window.location.hostname+"/forum",config='application/x-www-form-urlencoded';
        $http.post(url, JSON.stringify(data), config).then(function (response) {
                console.log(response);
        }, function (response) {
               console.log("server error");
            });
        console.log(data);
        $scope.new_post_text = "";
    }

    $scope.logout = function(){var cookies = document.cookie.split(";");for (var i = 0; i < cookies.length; i++){var cookie = cookies[i];var eqPos = cookie.indexOf("=");var name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";window.location.reload();}}
    
    $scope.get_details_about_post = function(comment_id){
       console.log(comment_id);
       
       // fetch  comment details from comment id 
   }

});