
(function () {
    'use strict'
  
  
    function on() {
     $("#overlay").css("display", "block");
    }
    
    function off() {
      $("#overlay").css("display", "none");
    }
  
    var forms = document.querySelectorAll('.needs-validation')
  
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms)
      .forEach(function (form) {
        form.addEventListener('keyup', function (event) {
          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
          }
          
          form.classList.add('was-validated')
        }, false)
      });
  
    $('form input').keyup(function() {
  
      var empty = false;
      var i = 0;
      $('form input').each(function() {
        i++;
        if(i == 3){
          return false;
        }
        if ($(this).val() == '') {
            empty = true;
        }
      });
      if (empty) {
          $('#saveButton').attr('disabled', 'disabled'); 
      } else {
          $('#saveButton').removeAttr('disabled'); 
      }
    });
  
    $("#form").submit(function(e) {
      on(); // show overlay.
      e.preventDefault(); // avoid to execute the actual submit of the form.
      var formData = {
        "is-new-file": false,
        "form-values": {
          "filename": $("#filename").val(),
          "access-key-id": $("#accessKeyId").val(),
          "access-key": $("#accessKey").val(),
          "endpoint": $("#endpoint").val(),
          "pathstyle": $("#pathstyle").val(),
          "skipssl": $("#skipssl").val(),
          "nossl": $("#nossl").val()
        }
      };    
  
      var actionUrl = "api/submit_credentials?filepath=" + $("#filepath").val();
      
      $.ajax({
          type: "POST",
          url: actionUrl,
          data: formData, // serializes the form's elements.
          dataType: "json",
          success: function(data){
            off(); // remove overlay.
            $('.backend-feedback').html("");
          },
          error: function(){
            off();
            $.getJSON('/static/fail-form-response.json', function(data){
              $('.backend-feedback').html("");
              $.each(data.issues, function(i, f){
                const title = f['error-title'];
                const message = f['error-message'];
                var error = title + ": " + message;
                if(f['input-name']=="filename"){
                  $('#filenameError').append(error);
                }
                if(f['input-name']=="access-key-id"){
                  $('#accessKeyIdError').append(error);
                }
                if(f['input-name']=="access-key"){
                  $('#accessKeyError').append(error);
                }
              })
            });
          }
      });
      
    });
    $("#form").dirty({
      preventLeaving: true
    });
  })()