var date = new Date();

$(document).ready(function() {
    
    $('.startDate').each(function() {
        $(this).val(new String(date.getFullYear())+"-"+(("0" + date.getMonth()).slice(-2))+"-"+date.getDate());
        $(this).datepicker(
        { dateFormat: 'yy-mm-dd' });
    });
    
    $("#save").click(function(){
        
       console.log("PICKED DATE " + $('.startDate').val()); 
    });
});
