// let start = null;
// let end = null;
// let draw = SVG().addTo('#svgCanvas');
//
// let img = document.getElementById('svgObject');
// let scaleX = img.naturalWidth / img.width;
// let scaleY = img.naturalHeight / img.height;
//
// $('#svgCanvas').click(function (e) {
//     let rect = e.target.getBoundingClientRect();
//     let x = e.clientX - rect.left;
//     let y = e.clientY - rect.top;
//
//     // Scale the coordinates
//     x = Math.round(x * scaleX);
//     y = Math.round(y * scaleY);
//
//     let circle = draw.circle(10);
//     circle.center(x, y);
//     circle.fill(start === null ? "green" : "red");
//
//     if (start === null) {
//         start = [Math.round(x), Math.round(y)];
//     } else if (end === null) {
//         end = [Math.round(x), Math.round(y)];
//     }
// });
//
// $('#findPathButton').click(function () {
//     if (start !== null && end !== null) {
//         $.ajax({
//             type: "POST",
//             url: '/find_path',
//             contentType: "application/json",
//             data: JSON.stringify({
//                 start: start,
//                 end: end
//             }),
//             dataType: "json",
//             success: function (response) {
//                 let path = response.path;
//                 for(let i=0; i<path.length; i++){
//                     let circle = draw.circle(3); // Create a small circle
//                     circle.center(path[i][0] / scaleX, path[i][1] / scaleY);
//                     circle.fill('blue'); // Color it blue
//                 }
//                 console.log(response)
//             }
//         });
//         start = null;
//         end = null;
//     }
// });

let qrCode = null;
let draw = SVG().addTo('#svgCanvas');

let img = document.getElementById('svgObject');
let scaleX = img.naturalWidth / img.width;
let scaleY = img.naturalHeight / img.height;

$('#qrCodeInput').change(function () {
    qrCode = $(this).val();
});

$('#setStartButton').click(function () {
    if (qrCode !== null) {
        $.ajax({
            type: "POST",
            url: '/set_start',
            contentType: "application/json",
            data: JSON.stringify({
                qr_code: qrCode
            }),
            dataType: "json",
            success: function (response) {
                console.log(response)
            }
        });
    }
});

$('#findPathButton').click(function () {
    let fromStore = document.getElementById('fromStoreCheckbox').checked;
    let url = '/find_path';
    let data = fromStore ? { from_store: true, qr_code: qrCode } : {};

    $.ajax({
        type: "POST",
        url: url,
        contentType: "application/json",
        data: JSON.stringify(data),
        dataType: "json",
        success: function (response) {
            let path = response.path;
            for(let i=0; i<path.length; i++){
                let circle = draw.circle(3); // Create a small circle
                circle.center(path[i][0] / scaleX, path[i][1] / scaleY);
                circle.fill('blue'); // Color it blue
            }
            console.log(response)
        }
    });
});

