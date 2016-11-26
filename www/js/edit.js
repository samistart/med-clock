
var STAGES = [
    {
        key : "enter_waiting_room",
        id : "enter-waiting-room"
    },
    {
        key : "leave_waiting_room",
        id : "leave-waiting-room",
    },
    {
        key : "nurse_begins_prep",
        id : "nurse-begins-prep",
    },
    {
        key : "begin_dialysis",
        id : "begin-dialysis",
    },
    {
        key : "end_dialysis",
        id : "end-dialysis",
    },
    {
        key : "nurse_applies_bandage",
        id : "nurse-applies-bandage",
    },
    {
        key : "enter_waiting_room_done",
        id : "enter-waiting-room-done"
    }
]

var ATTRIBUTES = [
    {
        key : "age",
        id : "age",
        parseFn : function(x) { return parseInt(x); } 
    },
    {
        key : "mode_of_transport",
        id : "mode-of-transport",
        parseFn : function(x) { return x; }
    },
    {
        key : "ward_area",
        id : "ward-area",
        parseFn : function(x) { return x; }
    },
    {
        key : "shift_of_the_day",
        id : "shift-of-the-day",
        parseFn : function(x) { return x; }
    },
    {
        key : "vascular_access",
        id : "vascular-access",
        parseFn : function(x) { return x; }
    },
    {
        key : "mobility_status",
        id : "mobility-status",
        parseFn : function(x) { return x; }
    },
    {
        key : "nurse_seniority",
        id : "nurse-seniority",
        parseFn : function(x) { return x; }
    }
];

// update patient attribute value
function updateVal( id, key, val ) {
    var data = {};
    data[ key ] = val;
    return qwest.put( "/api/patient/" + id, data )
        .then( function() {
            console.log( "updated: " + key + " to value: " + val + " for patient: " + id );
        })
        .catch( function(e) {
            console.log( "oops: " + e );
        });
}

// disable a stage timer button due to stage being completed
function disableButton( fullId ) {
    $( fullId )
        .prop( "disabled", true )
        .text( "Completed" )
        .css( { "color"  : "green" } );
}

$(document).ready(function() {

    var id = 5;

    qwest.get( "/api/patient/" + id )
        .then( function( xhr, patient ) {
            
            _.each( ATTRIBUTES, function( attr ) {
                $("#attr-" + attr.id)
                    .val( patient[ attr.key ] )
                    .on( "change", _.debounce(function() {
                        updateVal( attr.key, attr.parseFn( $(this).val() ) );
                    },500))
            });

            _.each( STAGES, function( stage ) {
                var fullId = "#stage-" + stage.id; 
                if( patient[ stage.key ] !== null )
                    disableButton( fullId );
                $( fullId )
                    .on( "click", function() {
                        disableButton( fullId );
                        updateVal( stage.key, moment().utc().format() );
                    });
            });

        });

});
