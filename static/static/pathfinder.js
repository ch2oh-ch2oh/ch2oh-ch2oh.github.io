let start = null;
let end = null;

$('#svgCanvas').click(function (e) {
    let svgElement = document.getElementById("svgCanvas");

    let matrix = svgElement.getScreenCTM();
    let point = svgElement.createSVGPoint();
    point.x = e.clientX;
    point.y = e.clientY;
    let svgPoint = point.matrixTransform(matrix.inverse());

    let x = svgPoint.x;
    let y = svgPoint.y;

    if (start === null) {
        start = [x, y];
    } else if (end === null) {
        end = [x, y];
    }
});


$('#findPathButton').click(function () {
    if (start !== null && end !== null) {
        $.ajax({
            type: "POST",
            url: '/find_path',
            contentType: "application/json",
            data: JSON.stringify({
                start: start,
                end: end
            }),
            dataType: "json",
            success: function (response) {
                let svgns = "http://www.w3.org/2000/svg";
                let svgCanvas = document.getElementById('svgCanvas');
                let path = response.path;
                for(let i = 0; i < path.length - 1; i++) {
                    let line = document.createElementNS(svgns, 'line');
                    line.setAttributeNS(null, 'x1', path[i][0]);
                    line.setAttributeNS(null, 'y1', path[i][1]);
                    line.setAttributeNS(null, 'x2', path[i+1][0]);
                    line.setAttributeNS(null, 'y2', path[i+1][1]);
                    line.setAttributeNS(null, 'style', 'stroke:rgb(255,0,0);stroke-width:2');
                    svgCanvas.appendChild(line);
                }
            }
        });
        start = null;
        end = null;
    }
});
