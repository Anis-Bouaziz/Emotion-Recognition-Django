let inputElement = document.getElementById('fileInput');
let inputElement2 = document.getElementById('fileInput2');
let imgElement = new Image();
let canvas = document.getElementById('canvasOutput');
let code = document.getElementById('code');
let pre = document.getElementById('pre');
let pic = document.getElementById("pic");
let vid = document.getElementById('video')
let viddiv = document.getElementById('viddiv')
let verifImg = document.getElementById('verifImg')


inputElement.addEventListener('change', (e) => {

    canvas.src = URL.createObjectURL(e.target.files[0]);
    canvas.hidden = false
}, false);
inputElement2.addEventListener('change', (e) => {

    verifImg.src = URL.createObjectURL(e.target.files[0]);
    verifImg.hidden = false
}, false);

function detectEmotions() {

    var formData = new FormData();
    formData.append('file', $('#fileInput').prop('files')[0]);
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

function detectMask() {

    var formData = new FormData();
    formData.append('file', $('#fileInput').prop('files')[0]);
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

function detectFaces() {

    var formData = new FormData();
    formData.append('file', $('#fileInput').prop('files')[0]);

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

function camera(param) {

    var check = new FormData();
    if (param.checked) {
        vid.src = "/api/camera"
        viddiv.hidden = false
        pic.hidden = true

    } else {
        check.append('cam', 0)
        $.ajax({
            type: 'POST',
            url: '/api/Close',
            data: check,
            dataType: "json",
            processData: false,
            contentType: false,

            success: function(response) {
                vid.src = "#"
                pic.hidden = false
            },
            error: console.log("error")
        })
    }
}

function VerifyFaces() {
    var formData = new FormData();
    formData.append('file', $('#fileInput').prop('files')[0]);
    formData.append('file2', $('#fileInput2').prop('files')[0]);

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