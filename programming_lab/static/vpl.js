function sidebar_setup() {
    // Enable the slide boxes
    $('.sidebar_box h3').click(function() {
        $(this).next().slideToggle('fast');
             });
    $('#classlist').load('/classlist/');
    $('#classlist').slideDown();
}

function show_projects_for_class(class_id) {
    $('#projectlist').load('/projects/list_for_class/' + class_id + '/');
    $('#projectlist').slideDown();
    $('#classlist a').removeClass('selected');
    $('#classlist_'+class_id).addClass('selected');
}

function show_files_for_project(project_id) {
    $('#filelist').load('/projects/files_for_project/' + project_id + '/');
    $('#filelist').slideDown();
    $('#projectlist a').removeClass('selected');
    $('#project_'+project_id).addClass('selected');
    var files = editAreaLoader.getAllFiles("code_editor");
    for (k in files) {
        editAreaLoader.closeFile("code_editor", k);
    }
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
