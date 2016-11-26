
var STAGES = [
    {
        key : "enter_waiting_room",
        query : "#enter-waiting-room"
    },
    {
        key : "leave_waiting_room",
        query : "#leave-waiting-room",
    },
    {
        key : "nurse_begins_prep",
        query : "#nurse-begins-prep",
    },
    {
        key : "begin_dialysis",
        query : "#begin-dialysis",
    },
    {
        key : "end_dialysis",
        query : "#end-dialysis",
    },
    {
        key : "nurse_applies_bandage",
        query : "#nurse-applies-bandage",
    },
    {
        key : "enter_waiting_room_done",
        query : "#enter-waiting-room-done"
    }
]

var ATTRIBUTES = [
    {
        key : "age",
        query : "#age",
        parseFn : function(x) { return parseInt(x); } 
    },
    {
        key : "transport_type",
        query : "#mode-of-transport",
        parseFn : function(x) { return x; }
    },
    {
        key : "ward_area",
        query : "#ward-area",
        parseFn : function(x) { return x; }
    },
    {
        key : "shift",
        query : "#shift-of-the-day",
        parseFn : function(x) { return x; }
    },
    {
        key : "vascular_access",
        query : "#vascular-access",
        parseFn : function(x) { return x; }
    },
    {
        key : "mobility",
        query : "#mobility-status",
        parseFn : function(x) { return x; }
    },
    {
        key : "nurse_seniority",
        query : "#nurse-seniority",
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

function setAttributes( id ) {
    return qwest.get( "/api/patient/" + id )
        .then( function( xhr, patient ) {
            console.log( "retrieved fresh set of attributes for: " + id );
            _.each( ATTRIBUTES, function( attr ) {
                $(attr.query)
                    .val( patient[ attr.key ] )
                    .unbind()
                    .on( "change", _.debounce(function() {
                        updateVal( id, attr.key, attr.parseFn( $(this).val() ) );
                    },500))
            });
        });
}

function setStages( id ) {

    return qwest.get( "/api/patient/" + id )
        .then( function( xhr, patient ) {
            console.log( "retrieved fresh set of stages for: " + id );
            _.each( STAGES, function( stage ) {
                var completed = patient[ stage.key ] !== null;
                var endTime = completed ? moment( patient[ stage.key ] ) : moment().utc();
                $( stage.query + " span" )
                    .val( endTime.format() );
                $( stage.query + " button" )
                    .prop( "disabled", completed )
                    .text( completed ? "Completed" : "Complete" )
                    .unbind()
                    .on( "click", function() {
                        updateVal( id, stage.key, moment().utc().format() )
                            .then( function() {
                                setStages( id );
                            });
                    });
            });

            setTimeout( function() {
                setStages( id );
            }, 1000 );

        });
}

$(document).ready(function() {

    var id = querystring.parse().id;
    $("#id-field").val( id );
    setAttributes( id );
    setStages( id );


});
