
Query(document).ready(function($) {

    $('#phone').mask('+7 (999) 999-99-99');
  
  });
  
  $(document).ready(function() {
  
      window.getMessage = function(form) {
          event.preventDefault();
  
          var form = $(form);
          var data = form.serializeArray();
  
          $.ajax({
              url: '../form.php',
              type: 'POST',
              data: data,
              success: function(result) {
                   $("#error").html(result);
                  if (result === 'error'){
                      $("#error").html("Введите данные в поля формы! ");
                  }
                  else{
                  form.fadeOut(500, function() {
                      $("#number").html('<h3>Поздравляем! <br>Вы успешно зарегистрированы на экскурсию!</h3> <h3 class="mt-4">Код вашей команды: ' + result +'</h3> ');
                      form.find('.form-control').val(' ');
  
                  });
                  
              }
              },
              error: function() {
                  $("#error").html("Введите данные в поля формы!");
              }
          });
  return false;
      }
  });  