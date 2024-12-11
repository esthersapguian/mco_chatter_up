$(document).ready(function(){
    var socket = io();
    

    socket.on('message',function(data){
    
        let username = data.username;
        let msg = data.msg;
        let timestamp = new Date(data.timestamp).toLocaleString(); //format the timestamp
        let messageClass = (username === sessionStorage.getItem('currentUser')) ? 'user1' : 'user2';
    
         $("#chat-box").append(
        `<div class="message ${messageClass}"><strong>${username}:</strong> ${msg}<div class="timestamp">${timestamp}</div></div>`
    );
       // $("#chat-box").append(`<div><strong>${username}:</strong> ${msg} </div>`)
    });
    $('#send-btn').on('click', function(){
        var message = $('#message').val();
        socket.send(message); //send message to the server
        $("#message").val(''); //clears the input field
    })
    $('#message').keypress(function(e){
        if (e.which == 13){
            $("#send-btn").click();
            return false;
        }
    })
    
});