$(function() {

    $('#search_book').keyup(function() {
        var q = $('#search_book').val();
        q = q.replace(/\s\s+/g, ' ');
        q = q.split(' ').join('+');
        

        console.log(q);
        $.ajax({
            type: "GET",
            url: "https://www.googleapis.com/books/v1/volumes?q=" + q,
            dataType: 'json',
            success: function(data){
                $('#search-results').fadeIn();  
                $("#hodo").html("");
                for (var i = 0; i < data.items.length; i++) {
                    var temp = '<a class="list-group-item"  data-something=' + data.items[i].id + '><strong>' + 
                    data.items[i].volumeInfo.title + '</strong></a>';

                    $("#hodo").append(temp);
               }
               // $('#search-results').html(q);  
           } ,
            
        });
    });

    
    $('#search-results').on('click', 'a', function(){  
         $.ajax({
            type: "GET",
            url: '/clients',
            dataType: 'json',
            success: function(data){
                $('#search-results').fadeIn();  
                $("#hodo").html("");
                for (var i = 0; i < data.items.length; i++) {
                    var temp = '<a class="list-group-item"  data-something=' + data.items[i].id + '><strong>' + 
                    data.items[i].volumeInfo.title + '</strong></a>';

                    $("#hodo").append(temp);
               }
               // $('#search-results').html(q);  
           } ,
            
        });
           
      }); 
});

function searchSuccess(data, textStatus, jqXHR)
{
    $('#search-results').fadeIn();  
    $('#search-results').html(data)
}


$(function() {

    $('#search_author').keyup(function() {
        $.ajax({
            type: "GET",
            url: "/author_search/",
            data: {
                'search_text' : $('#search_author').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess2,
            dataType: 'html'
        });
    });

    $('#search-author-results').on('click', 'a', function(){  
           $('#search_author').val('');
           $('#search-author-results').fadeOut();
           var inp = $('#authors').val();
           if (inp.length > 0 ) inp = inp + " ; "
           $('#authors').val( inp +  $(this).text()) ;
      }); 
});

function searchSuccess2(data, textStatus, jqXHR)
{
    $('#search-author-results').fadeIn();  
    $('#search-author-results').html(data)
}

