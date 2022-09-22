// скрипт для использования POST запроса в AJAX и DJANGO using JQuery
// получает из Cookie csrfToken и записывает его в headers html документа
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== ''){
//         let cookies = document.cookie.split(';');
//         for(let i = 0; i < cookies.length; i++){
//             let cookie = jQuery.trim(cookies[i]);
//             //Does this cookie string begin with the name we want?
//             if (cookie.substring(0, name.length + 1) === (name + '=')){
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }
// let csrftoken = getCookie('csrftoken');
// function csrfSafeMethod(method){
//     //this HTTP method do not require CSRF protection
//     return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
// }
// $.ajaxSetup({
//     beforeSend: function (xhr, settings) {
//         if (!csrfSafeMethod(settings.type) && !this.crossDomain){
//             xhr.setRequestHeader("X-CSRFToken", csrftoken);
//         }
//     }
// });
//================================================================

// load main content
function LoadMainContent() {
    $.ajax({
        type: "GET",
        url: "main_frame_content_get/",
        data: {
            // nothing
        },
        dataType: "html",
        cache: false,
        success: function (data) {
            // console.log(data);
            // alert(x);
            // document.getElementById("ajax_answer").innerHTML = data;
            $("#main_frame_content").html(data);
        }
    });
}

// load sub content
function LoadSubContent(tbl_tr) {
    let source_id = tbl_tr.innerText.at(0)
    $.ajax({
        type: "GET",
        url: "sub_frame_content_get/",
        data: {
            'source_id': source_id,
        },
        dataType: "html",
        cache: false,
        success: function (data) {
            $("#sub_frame_content").html(data);
        }
    });
}

//Listeners
addEventListener('DOMContentLoaded', (event) => {
    LoadMainContent.call();
});

$("#subitem_1_1").click(LoadMainContent);

$("#main_table tr").click(function(){
    LoadSubContent(this)
});
