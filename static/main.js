$(function() {
  console.log( "ready!" );
  $('.entry').on('click', function(){
    console.log("test")
    var entry = this;
    var post_id = $(this).find('h2').attr('id');
    var
    console.log(post_id)
    $.ajax({
      type:'GET',
      url: '/delete' + '/' + post_id,
      context: entry,
      success:function(result){
        if(result['status'] === 1){
          $(this).remove();
          console.log(result);
        }
      }
    });
  });
});
$('#submit').click(function(){
    var login = document.getElementById('login').value;
    var firstName = document.getElementById('firstName').value;
    var lastName = document.getElementById('lastName').value;

    var controllerPath = "/eventgate/users";
    $.post(controllerPath, $("#registrationForm").serialize(),
        function(){
        }
    ).error(function() { alert("Registration Failed"); }
    ).complete(function() {
        alert('Thank you ' + firstName + ' ' + lastName + ' for registering with EventGate. Your UserName for logging in is ' + login + '. No verification is required.');
    });
});
