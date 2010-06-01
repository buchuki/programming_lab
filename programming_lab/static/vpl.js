classlist_id = null;

function sidebar_setup() {
    // Enable the slide boxes
    $('.sidebar_box h3').click(function() {
        $(this).next().slideToggle('fast');
             });
    load_classlist($.url.param('classlist'));
    if ($.url.param('classlist')) {
        show_projects_for_class($.url.param('classlist'), $.url.param('projectlist'));
        if ($.url.param('projectlist')) {
            show_files_for_project($.url.param('projectlist'));
        }
    }
    // Ensure that user chat list is refreshed every minute
    window.setInterval(chat_users, 60000);
    chat_users();
}

function chat_users() {
    if (classlist_id == null) return;
    $('#userlist').load('/chat/logged_in_to_class/' + classlist_id + '/');

}

function ea_load(id) {
    // When the edit_area is finished loading, we may need to load a file
    // immediately depending on get parameters
    if ($.url.param('classlist') && $.url.param('projectlist') && $.url.param('file_id')) {
        load_file($.url.param('file_id'));
    }
}

function load_classlist(selected_id) {
    $('#classlist').load('/classlist/', {}, function() {
        if (selected_id) {
            select_class(selected_id);
        }
    });
    $('#classlist').slideDown();
}
function show_projects_for_class(class_id, selected_id) {
    $('#projectlist').load('/projects/list_for_class/' + class_id + '/', {}, function() {
        if (selected_id) {
            select_project(selected_id);
        }
            
    });
    $('#projectlist').slideDown();
    select_class(class_id);
}

function show_files_for_project(project_id) {
    $('#filelist').load('/projects/files_for_project/' + project_id + '/');
    $('#filelist').slideDown();
    select_project(project_id);
    var files = editAreaLoader.getAllFiles("code_editor");
    for (k in files) {
        editAreaLoader.closeFile("code_editor", k);
    }
}
function select_class(class_id) {
    $('#classlist a').removeClass('selected');
    $('#classlist_'+class_id).addClass('selected');
    classlist_id = class_id;
    chat_users();
}
function select_project(project_id) {
    $('#projectlist a').removeClass('selected');
    $('#project_'+project_id).addClass('selected');
}
function load_file(file_id) {
    $.ajax({
        url: '/projects/file/' + file_id + '/',
        dataType: "json",
        success: function(response) {
                editAreaLoader.openFile('code_editor', {
                    'id': response.id,
                    'title': response.title,
                    'text': response.text,
                    'syntax': response.syntax,
                    'do_highlight': true
                });
                editAreaLoader.execCommand('code_editor', 'set_editable', true);
        }
    });
}

function save_file(editor_id, contents) {
    var info = editAreaLoader.getCurrentFile(editor_id);
    $.ajax({
        url: '/projects/file/' + info.id + '/',
        type: 'POST',
        data: {'contents': contents},
        success: function(response) {
            editAreaLoader.setFileEditedMode('code_editor', info.id, false);
        }
    });
}
