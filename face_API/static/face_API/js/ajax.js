let inputElement = document.getElementById('fileInput');
let inputElement2 = document.getElementById('fileInput2');
let canvas = document.getElementById('canvasOutput');
let code = document.getElementById('code');
let pre = document.getElementById('pre');
let pic = document.getElementById("pic");
let vid = document.getElementById('video')
let viddiv = document.getElementById('viddiv')
let verifImg = document.getElementById('verifImg')
let imgsource1 = document.getElementById('imgsource1')
let imgsource2 = document.getElementById('imgsource2')
let modelpics = document.getElementById('modelpics')
let profilepicture = document.getElementById('profilepicture')
let userpic = document.getElementById('userpic1')
inputElement.addEventListener('change', (e) => {

    canvas.src = URL.createObjectURL(e.target.files[0]);
    imgsource1.src = URL.createObjectURL(e.target.files[0]);
    canvas.hidden = false
}, false);
inputElement2.addEventListener('change', (e) => {

    verifImg.src = URL.createObjectURL(e.target.files[0]);
    imgsource2.src = URL.createObjectURL(e.target.files[0]);
    verifImg.hidden = false
}, false);
modelpics.addEventListener('change', (e) => {
    if (e.target.files.length != 6) {
        alert('Please upload 6 pictures')

    } else {
        $('#modelpicscontainer').children().each((index, element) => {
            console.log(index)
            element.src = URL.createObjectURL(e.target.files[index]);
        });
    }



}, false);
profilepicture.addEventListener('change', (e) => {

    userpic.src = URL.createObjectURL(e.target.files[0]);

}, false);

async function detectEmotions() {
    verifImg.src = ""
    var img = await fetch(imgsource1.src)
    var blob = await img.blob()
    var file = await new File([blob], 'ex.jpg', blob)
    var formData = new FormData();
    formData.append('file', file);
    $.ajax({
        type: 'POST',
        url: '/face_API/emotion',
        data: formData,
        dataType: "json",
        processData: false,
        contentType: false,



        success: function(response) {

            canvas.src = "data:image/jpeg;base64," + response.image;
            code.innerHTML = "Total faces detected : " + response.total + "\n Json:\n" + prettyPrintJson.toHtml(response.json)
            pre.hidden = false
        },
        error: function(jqXHR, textStatus, error) {

            alert(jqXHR.responseText)
        }
    })
}

async function detectMask() {
    verifImg.src = ""
    var img = await fetch(imgsource1.src)
    var blob = await img.blob()
    var file = await new File([blob], 'ex.jpg', blob)
    var formData = new FormData();
    formData.append('file', file);
    $.ajax({
        type: 'POST',
        url: '/face_API/mask',
        data: formData,
        dataType: "json",
        processData: false,
        contentType: false,



        success: function(response) {

            canvas.src = "data:image/jpeg;base64," + response.image;
            code.innerHTML = "Total faces detected : " + response.total + "\n Json:\n" + prettyPrintJson.toHtml(response.json)
            pre.hidden = false
        },
        error: function(jqXHR, textStatus, error) {

            alert(jqXHR.responseText)
        }
    })
}
async function detectAttributes() {
    verifImg.src = ""
    var img = await fetch(imgsource1.src)
    var blob = await img.blob()
    var file = await new File([blob], 'ex.jpg', blob)
    var formData = new FormData();
    formData.append('file', file);
    $.ajax({
        type: 'POST',
        url: '/face_API/attributes',
        data: formData,
        dataType: "json",
        processData: false,
        contentType: false,



        success: function(response) {

            canvas.src = "data:image/jpeg;base64," + response.image;
            code.innerHTML = "Total faces detected : " + response.total + "\n Json:\n" + prettyPrintJson.toHtml(response.json)
            pre.hidden = false
        },
        error: function(jqXHR, textStatus, error) {

            alert(jqXHR.responseText)
        }
    })
}

async function detectFaces() {
    verifImg.src = ""
    var img = await fetch(imgsource1.src)
    var blob = await img.blob()
    var file = await new File([blob], 'ex.jpg', blob)
    var formData = new FormData();

    formData.append('file', file)
        //formData.append('file', $('#fileInput').prop('files')[0]);

    $.ajax({
        type: 'POST',
        url: '/face_API/faces',
        data: formData,
        dataType: 'json',
        processData: false,
        contentType: false,
        success: function(response) {
            canvas.src = "data:image/jpeg;base64," + response.image;
            code.innerHTML = "Total faces detected : " + response.total + "\n Json:\n" + prettyPrintJson.toHtml(response.json)
            pre.hidden = false
        },
        error: function(jqXHR, textStatus, error) {

            alert(jqXHR.responseText)
        }
    })

}

async function VerifyFaces() {
    var img = await fetch(imgsource1.src)
    var blob = await img.blob()
    var file1 = await new File([blob], 'ex.jpg', blob)

    var img = await fetch(imgsource2.src)
    var blob = await img.blob()
    var file2 = await new File([blob], 'ex2.jpg', blob)

    var formData = new FormData();
    formData.append('file', file1);
    formData.append('file2', file2);

    $.ajax({
        type: 'POST',
        url: '/face_API/verify',
        data: formData,
        dataType: "json",
        processData: false,
        contentType: false,



        success: function(response) {
            verifImg.src = "data:image/jpeg;base64," + response.image2;
            canvas.src = "data:image/jpeg;base64," + response.image1;
            code.innerHTML = prettyPrintJson.toHtml(response.json)
            pre.hidden = false
        },
        error: function(jqXHR, textStatus, error) {

            alert(jqXHR.responseText)
        }
    })
}
/***********************************************************************/
jQuery(function($) {

    $(".sidebar-dropdown > a").click(function() {
        $(".sidebar-submenu").slideUp(200);
        if (
            $(this)
            .parent()
            .hasClass("active")
        ) {
            $(".sidebar-dropdown").removeClass("active");
            $(this)
                .parent()
                .removeClass("active");
        } else {
            $(".sidebar-dropdown").removeClass("active");
            $(this)
                .next(".sidebar-submenu")
                .slideDown(200);
            $(this)
                .parent()
                .addClass("active");
        }
    });

    $("#close-sidebar").click(function() {
        $(".page-wrapper").removeClass("toggled");
    });
    $("#show-sidebar").click(function() {
        $(".page-wrapper").addClass("toggled");
    });




});


/***********************************************************/

const video = document.getElementById('webcam');
const canvasElement = document.getElementById('canvas');


function Modal() {
    document.getElementById('id01').style.display = 'block'
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                video.srcObject = stream;
            })
            .catch(function(err0r) {
                console.log("Something went wrong!");
            });

    }

}

function Signup_Modal() {
    document.getElementById('id02').style.display = 'block'

}
// Get the modal
var modal = document.getElementById('id01');
var modal2 = document.getElementById('id02');
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
        stream = video.srcObject;
        stream.getTracks().forEach(function(track) {
            track.stop();
        });
    }
    if (event.target == modal2) {
        modal2.style.display = "none";
    }
}
$("#submit").click(function(e) {
    e.preventDefault()
        /* set the canvas to the dimensions of the video feed */
    canvasElement.width = video.videoWidth;
    canvasElement.height = video.videoHeight;
    /* make the snapshot */
    canvasElement.getContext('2d').drawImage(video, 0, 0, canvasElement.width, canvasElement.height);
    var img = canvasElement.toDataURL("image/jpeg");
    var blobBin = atob(img.split(',')[1]);
    var array = [];
    for (var i = 0; i < blobBin.length; i++) {
        array.push(blobBin.charCodeAt(i));
    }
    var file = new Blob([new Uint8Array(array)], { type: 'image/png' });
    var formdata = new FormData();
    formdata.append('file', file);
    /* username */
    var username = document.getElementById('username').value
    formdata.append('username', username);
    $.ajax({
        type: 'POST',
        url: '/face_API/Facelogin',
        data: formdata,

        processData: false,
        contentType: false,
        success: function(response) {
            location.reload()
        },
        error: function(jqXHR, textStatus, error) {

            alert(jqXHR.responseText)
        }
    })

})

$("#signup").click(function(e) {
    e.preventDefault()
    var files = document.getElementById('modelpics').files
    var profilepic = document.getElementById('profilepicture').files[0]
    var formdata = new FormData();

    for (let i = 0; i < files.length; i++) {
        formdata.append(i, files[i])
    }
    /* username and email*/
    var username = document.getElementById('signup_username').value
    var email = document.getElementById('email').value
    formdata.append('Profilepicture', profilepic)
    formdata.append('email', email);
    formdata.append('username', username);
    $.ajax({
        type: 'POST',
        url: '/face_API/Facesignin',
        data: formdata,

        processData: false,
        contentType: false,
        success: function(response) {
            location.reload()



        },
        error: function(jqXHR, textStatus, error) {

            alert(jqXHR.responseText)
        }
    })
})
var $loading = $('#loading').hide();
$(document)
    .ajaxStart(function() {
        $loading.show();
    })
    .ajaxStop(function() {
        $loading.hide();
    });
/*****************************************************/
var chatroom = new window.Chatroom({
    host: "http://localhost:5005",
    title: "Chat with Zara",
    container: document.querySelector(".chat-container"),
    welcomeMessage: "Hi, I am Zara. How may I help you?",
    speechRecognition: "en-US",
    voiceLang: "en-US"
});
chatroom.openChat();