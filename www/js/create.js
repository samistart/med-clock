$(document).ready(function() {
    $("#create")
        .on( "click", function() {
            qwest.post( "/api/patient" )
                .then( function( xhr, id ) {
                    window.location = "/www/html/edit.html?id=" + id;
                })
                .catch( function( e ) {
                    console.log( "oops: " + e );
                });
        });
});
