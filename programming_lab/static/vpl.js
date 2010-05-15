function sidebar_setup() {
    // Enable the slide boxes
    $('.sidebar_box h3').click(function() {
        $(this).next().slideToggle('fast');
             });
    $('#classlist').load('/classlist/');
    $('#classlist').slideDown();
}

function  show_projects_for_class(class_id) {
    $('#projectlist').load('/projects/list_for_class/' + class_id + '/');
    $('#projectlist').slideDown();
    $('#classlist a').removeClass('selected');
    $('#classlist_'+class_id).addClass('selected');
}
