$(document).ready(function(){
    $('#search').keyup(function(e) {
        str = e.target.value.toLowerCase();
        titles = ($('.prod-title'))
        //alert(str)
        titles.each(function(){
            //alert($(this).text())
            if(!$(this).text().toLowerCase().includes(str))$(this).parent().parent().parent().hide();
            else $(this).parent().parent().parent().show();
        })
        
    });

    $('.orderbutton').click(function(e) {
        e.preventDefault();
        if (window.confirm("Are you sure?")) {
            window.location = 'PlaceOrder';
        }
    });
  });

