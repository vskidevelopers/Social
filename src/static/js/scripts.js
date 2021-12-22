$(document).ready(function(){
    console.log("Working")
    $('#modal-btn').click(function(){
        console.log('working')
        $('.ui.modal')
        .modal('show')
        ;
    })
})

$(function() {
    new WOW().init();
})