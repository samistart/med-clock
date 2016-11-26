$(document).ready(function() {
    qwest.setDefaultDataType( "json" );
    $("#create")
        .on( "click", function() {
            var mac = $("#mac").val();
            var args = mac ? { mac_address : mac } : {};
            qwest.post( "/api/patient", args )
                .then( function( xhr, id ) {
                    window.location = "/www/html/edit.html?id=" + id;
                })
                .catch( function( e ) {
                    console.log( "oops: " + e );
                });
        });
});
