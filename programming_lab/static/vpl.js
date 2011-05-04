classlist_id = null;
lab_id = null;
chat_user_id = null;
code_editor = null;
current_project = null;
current_file = null;

function sidebar_setup() {
    $.ajaxSetup({cache: false}); //Internet Explorer is a bit fuddy...
    // Enable the slide boxes
    $('.sidebar_box h3').click(function() {
        $(this).next().slideToggle('fast');
             });
    load_classlist();
    load_labs();
    // Ensure that user chat list is refreshed every minute
    window.setInterval(chat_users, 5000);
    // Ensure that user chat messages are refreshed every 5 seconds
    window.setInterval(chat_messages, 5000);
    chat_users();
    $.ctrl('S', save_file);
}

function chat_users() {
    if (classlist_id != null) {
        $('#userlist').load('/chat/logged_in_to_class/' + classlist_id + '/');
    }
    else if (lab_id != null) {
        $('#userlist').load('/chat/logged_in_to_lab/' + lab_id + '/');
    }
}
function chat_messages() {
    if (chat_user_id == null) return;
    $('#chat_messages').load('/chat/chat_messages/' + chat_user_id + '/',
            function(response, textStatus, xmlrequest) {
                reset_chat();
            });
}
/* codemirror callbacks */
function editor_changed(editor) {
    if (current_file != null) {
        $("#file_" + file_id(current_file)).addClass('modified');
    }
}

function ea_load(id) {
    // This is an ea callback that needs to be replaced
    // When the edit_area is finished loading, we may need to load a file
    // immediately depending on get parameters
    if ($.url.param('projectlist') && $.url.param('filename')) {
        load_file($.url.param('projectlist'), $.url.param('filename'));
    }
}
/* end codemirror callbacks */

function load_classlist(selected_id) {
    $('#classlist').load('/classlist/', {}, function() {
        if ($('#classlist ul').children().length > 0) {
            $('#classlist_item').show();
        }
        if ($.url.param('classlist')) {
            show_projects_for_class($.url.param('classlist'), $.url.param('projectlist'));
        }
        if ($.url.param('projectlist')) {
            show_files_for_project($.url.param('projectlist'));
        }
    });
}
function load_labs() {
    $('#labs').load('/lab/', {}, function() {
        if ($.url.param('lab')) {
            show_projects_for_lab($.url.param('lab'), $.url.param('projectlist'));
        }
        if ($.url.param('projectlist')) {
            show_files_for_project($.url.param('projectlist'));
        }
    });
}
function show_projects_for_class(class_id, selected_id) {
    $('#projectlist').load('/projects/list_for_class/' + class_id + '/', {}, function() {
        if (selected_id) {
            select_project(selected_id);
        }
        else {
            $('#filelist').html("");
            close_files();
        }
            
    });
    $('#projectlist').slideDown();
    $('#userlist').slideDown();
    select_class(class_id);
}
function show_projects_for_lab(lab_id, selected_id) {
    $('#projectlist').load('/projects/list_for_lab/' + lab_id + '/', {}, function() {
            if (selected_id) {
                select_project(selected_id);
            }
            else {
                $('#filelist').html("");
                close_files();
            }
            });
            $('#projectlist').slideDown();
            $('#userlist').slideDown();
            select_lab(lab_id);
}
function show_files_for_project(project_id, keepopen) {
    $('#filelist').load('/projects/files_for_project/' + project_id + '/');
    $('#filelist').slideDown();
    $('#project_menu').load('/projects/menu_for_project/' + project_id + '/');
    select_project(project_id);
    if (!keepopen) {
        close_files();
    }
}
function close_files() {
    /* noop */
}
function select_class(class_id) {
    $('#breadcrumbs').html('Class: ' + $('#classlist_' + class_id).text());
    $('#participants_header').html('Class Participants');
    $('#projects_header').html('Class Projects');
    classlist_id = class_id;
    lab_id = null;
    chat_users();
}
function select_lab(l_id) {
    $('#breadcrumbs').html('Lab: ' + $('#lab_' + l_id).text());
    $('#participants_header').html('Lab Participants');
    $('#projects_header').html('Lab Projects');
    lab_id = l_id;
    classlist_id = null;
    chat_users();
}
function select_project(project_id) {
    current_project = project_id;
    $('#project_item').show();
    $('#projectlist a').removeClass('selected');
    $('#project_'+project_id).addClass('selected');
}
function load_file(project_id, filename) {
    current_file = null;
    $.ajax({
        url: '/projects/file/' + project_id + '/' + filename + '/',
        dataType: "json",
        success: function(response) {
            console.log(response);
                mirror = code_editor.mirror;
                mirror.setValue(response.text);
                current_file = filename;
                mirror.setOption("readOnly", false);
                mirror.setOption("mode", response.syntax);
                $('#filelist a').removeClass('selected');
                $('#file_'+file_id(filename)).addClass('selected');
                $('#file_menu').load('/projects/file_menu/' + escape(response.id) + '/', {},
                    function() {
                        if ($('#file_menu ul').children().length > 0) {
                            $('#file_item').show();
                        }
                    }
                );
        }
    });
}

function save_file() {
    if (current_file) {
        var contents = code_editor.mirror.getValue();
        $.ajax({
            url: '/projects/file/' + current_project + '/' + current_file + '/',
            type: 'POST',
            data: {'contents': contents},
            success: function(response) {
                $("#file_" + file_id(current_file)).removeClass("modified");
            }
        });
    }
}

function view_file(url, filename, wrap_js) {
    if (wrap_js) {
        filename = filename + "?wrapjs=wrap";
    }
    window.open(url + filename);
}
function view_shared_file(project_id, filename) {
    window.open('/projects/view_shared_file/' + project_id + '/' + filename + '/');
}

function compile_project(project_id) {
    $('#compile_output').html("Compiling, Please Wait...");
    $('#compile_output').slideDown();
    $('#compile_output').load('/projects/compile/' + project_id + '/', undefined,
            function (response, textStatus, xmlrequest) {
                show_files_for_project(project_id, keepopen=true);
            }
            );
}

function load_chat_box(user_id) {
    chat_user_id =user_id;
    chat_messages();
    $('#chat_input_box').show();
    $('#chatbox').slideDown();
    $('#chat_input').focus();
}

function reset_chat() {
    $("#chat_messages").animate({ scrollTop: $("#chat_messages").attr("scrollHeight") - $('#chat_messages').height() }, 200);
}
function send_chat_message() {
    $('#chat_messages').load(
            '/chat/chat_messages/' + chat_user_id + '/',
            {'message': $('#chat_input').val()},
            function(response, textStatus, xmlrequest) {
                reset_chat();
                $('#chat_input').focus();
            });
    $('#chat_input').val('');
    return false;
}
function share_file() {
    var info = editAreaLoader.getCurrentFile("code_editor");

    $('#chat_messages').load(
        "/chat/share_file/",
        {'file_id': info.id, 'share_to': chat_user_id},
        function(response, textStatus, xmlrequest) {
            reset_chat();
            $('#chat_input').focus();
        });
}

/* helpers */
function file_id(filename) {
    return filename.replace(/(:|\.)/g,'\\$1');

}

/* jquery plugin */
$.ctrl = function(key, callback, args) {
    $(document).keydown(function(e) {
        if(!args) args=[]; // IE barks when args is null
        if(e.keyCode == key.charCodeAt(0) && e.ctrlKey) {
            callback.apply(this, args);
            return false;
        }
    });
};
