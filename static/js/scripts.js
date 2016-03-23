(function($) {
    var $textarea = $("#id_message");

    $("#email_form").submit(function(e){
        if($("#id_subject").val() == ""){
            a = confirm("Are you sure you want to send an email without subject?");
            return a;
        }

        $textarea.val(function(i,val) {
            return $('<div>').html(val).text();
        });
      
    });

    $(".bold").click(function(){
        $textarea.val($textarea.val() + "[strong][/strong]")
    });

    $(".italic").click(function(){
        $textarea.val($textarea.val() + "[i][/i]")
    });

    $(".underline").click(function(){
        $textarea.val($textarea.val() + "[u][/u]")
    });

    $("#font-color").change(function(){
        var val = $(this).find("option:selected").val();
        $textarea.val($textarea.val() + "[font color='" + val + "'][/font]")
    });

}(jQuery));