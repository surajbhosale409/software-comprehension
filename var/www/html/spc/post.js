function reply(commentId) {
    var text_box_id = "#"+commentId+"_textarea_reply_div"
    $(text_box_id).show();
    //$("#"+commentId).hide(); 
    $("[id="+commentId+"]").hide();
}

function submit_reply(commentId, parentId) {
    commentid = commentId.split('_')[0]
    var reqData = {}
    reqData["email"] = localStorage.getItem('email');
    reqData["PostText"] = $("#"+commentid+"_textarea_reply").val();
    reqData["PostType"] = "Child";
    reqData["parent_id"] = commentid;

    $.post("forum/", JSON.stringify(reqData), function(response, status){
        angular.element('#mycontroller').scope().get_details_about_post(parentId);
        angular.element('#mycontroller').scope().$apply();
    });
}

function edit(commentId) {
    var text_box_id = "#"+commentId+"_textarea_edit_div";
    $(text_box_id).show();
    $("[id="+commentId+"]").hide();
    $("#"+commentId+"_post").hide(); 
}

function submit_edit(commentId, parentId){
    commentid = commentId.split('_')[0]
    var reqData = {}
    reqData["CommentId"] = commentid;
    reqData["PostText"] = $("#"+commentid+"_textarea_edit").val();

    $.ajax({
        url: 'forum/',
        type: 'PUT',
        data: JSON.stringify(reqData),
        contentType: 'application/json',

        success: function(result) {
            angular.element('#mycontroller').scope().get_details_about_post(parentId);
            angular.element('#mycontroller').scope().$apply();
        }
    });
}
export { edit, submit_edit, reply, submit_reply };

/*
var app = angular.module('myApp', ['ui.bootstrap']);
app.controller('myCtrl', function($rootScope, $scope, $http, $timeout, $interval, $q) {
    $scope.username = localStorage.getItem('username');
    $scope.email = localStorage.getItem('email');

    $scope.index_page = true
    $scope.AllTopics = []
    $scope.treedata = new Array();
    $scope.textBoxShow = false;

    $rootScope.reload = function(){
        window.location.reload();
    }

    $scope.create_new_post = function(){
        $http(
            {
                url: "forum/",
                method: 'POST',
                data: {
                    email: $scope.email,
                    PostText: $scope.new_post,
                    PostType: "Parent"
                }
            }
        ).then(
            function(response) {
                console.log(response)
                alert("Success")
            },
            function(response) {
                console.log(response)
            }     
        ) 
        $scope.new_post = "";
    }

    $scope.get_details_about_post = function(comment_id){
        $scope.index_page = false;

        $http(
            {
                url: "forum/",
                method: 'GET',
                params: {
                    commentid: comment_id
                }
            }
        ).then(
            function(response) {
                //$scope.treedata[0] = response.data.responseData;
                document.getElementById("post_and_comments_div").innerHTML = response.data;
                console.log(response)
            },
            function(response) {
                console.log(response)
            }     
        ) 
    }

    $scope.getAllTopics = function(){
        console.log("Entered")
        $http(
            {
                url: "forum/",
                method: 'GET',
            }
        ).then(
            function(response) {
                $scope.AllTopics = response.data.responseData;
            },
            function(response) {
                console.log(response)
            }     
        ) 
    }

    $interval(function () {
        $scope.getAllTopics();
    }, 9 *60 * 60);

    $scope.logout = function(){
        localStorage.clear();
        window.location.href = "http://myforum.com/index.html";
    }
})
*/
