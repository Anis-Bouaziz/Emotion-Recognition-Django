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
let imgsource1 = document.getElementById('imgsource1')
let imgsource2 = document.getElementById('imgsource2')

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

async function detectEmotions() {
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

async function detectFaces() {
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