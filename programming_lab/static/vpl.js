/*
# This file is part of Virtual Programming Lab.
# 
# Virtual Programming Lab is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Virtual Programming Lab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Virtual Programming Lab.  If not, see <http://www.gnu.org/licenses/>.
*/

classlist_id = null;
lab_id = null;
chat_user_id = null;
code_editor = null;
current_project = null;
current_file = null;
open_files = {};


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
            if ($.url.param('filename')) {
                show_files_for_project($.url.param('projectlist'),
                    selected_id=$.url.param('filename'));
            }
            else {
                show_files_for_project($.url.param('projectlist'));
            }
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
function idify() {
    return this.id;
}
function show_files_for_project(project_id, selected_id, keepopen) {
    var selected = $('#filelist a.selected').map(idify).get();
    var modified = $('#filelist a.modified').map(idify).get();
    $('#filelist').load('/projects/files_for_project/' + project_id + '/',
        function(response, textstatus,xhr) {
            if (selected_id) {
                load_file(project_id, selected_id);
            }
            if (keepopen) {
                $.each(selected, function(){
                    $('#' + file_id(this)).addClass("selected");
                });
                $.each(modified, function(){
                    $('#' + file_id(this)).addClass("modified");
                });
            }
    });
    $('#filelist').slideDown();
    $('#project_menu').load('/projects/menu_for_project/' + project_id + '/');
    select_project(project_id);
    if (!keepopen) {
        close_files();
    }
}
function close_files() {
    $('#file_item').hide();
    current_file = null;
    code_editor.mirror.setValue('');
    code_editor.mirror.setOption("readOnly", true);
    open_files = {};
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
    if (current_file && open_files[project_id + '/' + current_file]) {
        open_files[project_id + '/' + current_file].text = code_editor.mirror.getValue();
    }

    current_file = null;

    if (open_files[project_id + '/' + filename]) {
        var r = open_files[project_id + '/' + filename];
        setup_file(r, project_id, filename);
    }
    else {
        $.ajax({
            url: '/projects/file/' + project_id + '/' + filename + '/',
            dataType: "json",
            success: function(response) {
                    setup_file(response, project_id, filename);
            }
        });
    }
}

function setup_file(response, project_id, filename) {
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
    open_files[project_id + '/' + filename] = response;
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
                show_files_for_project(project_id, null, keepopen=true);
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
    if (!current_file) {
        return;
    }
    $('#chat_messages').load(
        "/chat/share_file/",
        {
            'file_id': current_project + "/" + current_file,
            'share_to': chat_user_id
        },
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
