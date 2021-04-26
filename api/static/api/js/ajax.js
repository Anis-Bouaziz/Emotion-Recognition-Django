let inputElement = document.getElementById('fileInput');
let imgElement = new Image();
let canvas = document.getElementById('canvasOutput');
let code = document.getElementById('code');
let pre = document.getElementById('pre');
let pic = document.getElementById("pic");
let vid = document.querySelector('video');
let viddiv = document.getElementById('viddiv')
let t;

const constraints = {
    video: true,
};

inputElement.addEventListener('change', (e) => {

    canvas.src = URL.createObjectURL(e.target.files[0]);
    canvas.hidden = false
}, false);




function detectEmotions() {

    var formData = new FormData();
    formData.append('file', $('#fileInput').prop('files')[0]);
    $.ajax({
        type: 'POST',
        url: '/api/predict',
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
        url: '/api/faces',
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




let cnv = document.getElementById('draw');
let context = cnv.getContext('2d');


function camera(param) {



    if (param.checked) {
        let s = navigator.mediaDevices.getUserMedia(constraints)
        canvas.hidden = true
        cnv.hidden = false
        viddiv.hidden = false
        pic.hidden = true
        pre.hidden = false
        s.then((stream) => {

            window.localStream = stream
            vid.srcObject = stream;
            vid.addEventListener('loadedmetadata', function() {

                cnv.width = this.videoWidth
                cnv.height = this.videoHeight

            })
            t = window.setInterval(function() {
                let imageCapture = new ImageCapture(stream.getTracks()[0])
                imageCapture.takePhoto({ imageWidth: cnv.width }).then(blob => {

                    let formData = new FormData();
                    formData.append('file', blob);
                    $.ajax({
                        type: 'POST',
                        url: '/api/camera',
                        data: formData,
                        dataType: "json",
                        processData: false,
                        contentType: false,


                        success: function(response) {

                            if (vid.srcObject) {

                                response.json.forEach(({ box: { top, left, width, height }, emotion, probability }) => {




                                    context.clearRect(0, 0, cnv.width, cnv.height);
                                    context.font = "25px Arial";
                                    context.fillStyle = "red";
                                    context.beginPath();
                                    context.rect(top, left, width, height);
                                    context.lineWidth = 2;
                                    context.strokeStyle = 'green';
                                    context.stroke();
                                    context.fillText(emotion + ' ' + probability.substr(0, 4), +top, +left);

                                });

                                code.innerHTML = "Total faces detected : " + response.total + "\n Json:\n" + prettyPrintJson.toHtml(response.json)

                            }

                        }
                    })



                })




            }, 700)



        });
    } else {
        localStream.getTracks().forEach(function(track) {
            track.stop();

        });

        canvas.hidden = false
        pre.hidden = true
        pic.hidden = false
        vid.srcObject = null
        canvas.src = ""
        window.clearInterval(t)
        t = 0

        context.clearRect(0, 0, cnv.width, cnv.height);
        cnv.hidden = true
        viddiv.hidden = true

    }
};