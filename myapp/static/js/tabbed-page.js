<<<<<<< HEAD
$(document).ready(function(){
    $(".S3").click();
  
    $(".storage-tab").click(function(){
      const provider = $(this).attr("provider")
      const filename = $(this).attr("filename")
      window.history.pushState("", "title", "/load-tabbed-page?provider="+provider+"&filename="+filename);
=======
$(window).on('load', function(){
  const getUrlParameter = function getUrlParameter(sParam) {
    let sPageURL = window.location.search.substring(1),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
        }
    }
    return false;
  };
  let dict = {}
  $(".storage-tab").click(function(){
    const provider = $(this).attr("provider");
    const filename = $(this).attr("filename");
    
    if(!(dict[filename] == 1 && dict[provider] == 1)){ // Check same filename in different provider
      $(".storage-tab").removeClass("active");
      $(this).addClass("active");
      window.history.pushState("", "title", "/tabbed-page?provider="+provider+"&filename="+filename);
>>>>>>> f768c84d6466a847ef02fe191112707ac4fa9b4e
      $.ajax({
        url: "/api/generate-tabbed-content",
        type: "get", //send it through get method
        data: { 
          provider: provider,
          file: filename
        },
        success: function(response) {
          //Do Something
          $("#nav-tabContent").html(response)
        },
        error: function(xhr) {
          //Do Something to handle error
        }
      });
<<<<<<< HEAD
    });
  });
  
  
=======
      dict = {}
      dict[filename] = 1;
      dict[provider] = 1;
    }
    
  });

  const req_provider = getUrlParameter('provider');
  const req_filename = getUrlParameter('filename');
  const req_provider_count = $(`#${req_provider} #list-tab .storage-tab`).length;
  let files = [];
  if(req_provider_count){
    $(`#${req_provider} #list-tab .storage-tab`).each(function () {
      files.push(this.id);
    });
  }

  if(req_provider && req_provider_count && ($.inArray(req_filename, files) != -1)){
    $(`.${req_provider}`).click();
    $(`#${req_provider} #${req_filename}`).addClass("active");
  }
  else{
    let providers = [];
    $('.accordion-collapse').each(function () {
        providers.push(this.id);
    });
    $.each(providers, function(key, provider) {
      let count = $(`#${provider} #list-tab .storage-tab`).length;
      if(count){
        $(`.${provider}`).click();
        $(".storage-tab:first").addClass("active");
        const filename = $(".storage-tab:first").attr("id");
        window.history.pushState("", "title", "/tabbed-page?provider="+provider+"&filename="+filename);
        return false;
      }
    });
  }
});

>>>>>>> f768c84d6466a847ef02fe191112707ac4fa9b4e
