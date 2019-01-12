$(function () {
        bindRegister();
    });
    function changImg(self) {
        self.src = self.src + '?';
    }
    function bindRegister() {
        $('#submit').click(function () {
            $('#error_msg').addClass('hide');
            $.ajax({
                url:'{% url "register" %}',
                type:'POST',
                data:$('#fm').serialize(),
                dataType:'JSON',
                success:function (arg) {
                    console.log(arg);
                    if(arg.status){
                        window.location.href = '{% url "login" %}';
                    }
                    else{
                        var $msg = arg.errors;
                        console.log($msg);
                        if ($msg['username']){
                            console.log($msg['username']);
                            $('#error_msg').text($msg['username'][0]);
                            $('#error_msg').removeClass('hide');
                        }
                        else if ($msg['email']){
                            console.log($msg['email']);
                            $('#error_msg').text($msg['email'][0]);
                            $('#error_msg').removeClass('hide');
                        }
                        else if($msg['pwd']){
                            console.log($msg['pwd']);
                            $('#error_msg').text($msg['pwd'][0]);
                            $('#error_msg').removeClass('hide');
                        }
                        else if ($msg['__all__']){
                            $('#error_msg').text($msg['__all__'][0]);
                            $('#error_msg').removeClass('hide');
                        }
                        else if ($msg['check_code']){
                            $('#error_msg').text($msg['check_code'][0]);
                            $('#error_msg').removeClass('hide');
                        }
                    }
                }
            })
        })
    }
