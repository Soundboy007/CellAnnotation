//JavaScript source code


/*
Loads TA annotated image onto one canvas and lifeact original imge onto another canvas
Toggling 'Z' key switches between brush and eraser
After Annotation, press 'S' key to read the annotated pixels into a list
Press the Submit button to send the list for retrieving and finishing the task
*/

window.addEventListener('load', () => {

    const canvas = document.querySelector("#canvas");
    const ctx = canvas.getContext("2d");

    const canvas2 = document.querySelector('#canvas2');
    const ctx2 = canvas2.getContext("2d");

    const img = new Image();
    const img2 = new Image();
    
	img.src = 'merged_U0000_L0000.jpg';
	img2.src = 'embryo-d_lifeact_000_U0000_L0000.jpg';

    canvas.height = 550;
    canvas.width = 550;
    ctx.strokeStyle = "#d7d1d2";
    ctx.lineWidth = 1;

    canvas2.height = 550;
    canvas2.width = 550;

    var dots = [];
    var mousedown = false;
    var norm = true;
    var brush_size = 20;
    
    img.onload = () => {

        ctx2.drawImage(img2, 0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

        canvas.addEventListener('mousedown', startPosition);
        canvas.addEventListener('mousemove', updateLine);
        canvas.addEventListener('mouseup', finishedPosition);     
    };

    turkSetAssignmentID();

    norm = true;
    canvas.addEventListener('mousedown', startPosition);
    canvas.addEventListener('mousemove', updateLine);
    canvas.addEventListener('mouseup', finishedPosition); 

    ///DEFAULT POSITIONS OF THE MOUSE EVENTS
    function startPosition(e) {
        mousedown = true;
        dots.push('none');
        dots.push('none');
    };

    /// DEFAULT POSITIONS OF THE MOUSE EVENTS
    function finishedPosition(e) {
        mousedown = false;
        dots.push('none');
        dots.push('none');

        ctx.beginPath();
    };


    ///DRAWING ON THE CANVAS
    function updateLine(e) {

        /// adjusting mouse position
        var r = canvas.getBoundingClientRect(),
            x = Math.trunc(e.clientX - r.left),
            y = Math.trunc(e.clientY - r.top);

        if (mousedown == false) return;
        if (!norm) return;
        ctx.lineCap = 'round';
        ctx.strokeStyle = "#d7d1d2";

        ctx.lineTo(x, y);
        ctx.stroke();

        dots.push(x, y);        
        ctx.beginPath();
        ctx.moveTo(x, y);
    }


    ///FUNCTION TO UNDO THE LAST PIXEL ANNOTATION
    /*function clearpath(e){
        //if (!norm) return;
        dots.pop(-1);
        dots.pop(-2);
        ctx.beginPath();

        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        ctx2.drawImage(img2, 0, 0, canvas.width, canvas.height);

        for(var i=0, len = dots.length-1; i < len; i+=2){
            if(dots[i] == 'none'){
                ctx.beginPath();
                }          

            ctx.lineTo(dots[i],dots[i+1]);
            ctx.stroke();
            ctx.beginPath();
            ctx.moveTo(dots[i],dots[i+1]);
        }

        ctx.beginPath();
        ctx2.beginPath();
    }*/


    ///CONVERTS RGB TO HEX CODE:
    function rgbToHex(r, g, b) {
        if (r > 255 || g > 255 || b > 255)
            throw "Invalid color component";
        
        return ((r << 16) | (g << 8) | b).toString(16);
    }


    ///ERASING WHITE PIXEL ANNOTATIONS FROM THE ORIGINAL IMAGE
    function erase_pixels(e){

        if (norm) return;
        //console.log('erase_pixels called');

        canvas.addEventListener('mousedown', function(){
            mousedown = true;
        }); 

        canvas.addEventListener('mouseup', function(){
            mousedown = false;
        }); 

        canvas.addEventListener('mousemove', function(e){
            
            if (mousedown == false) return;
            if (norm) return;

            // mousedown = true;
            //brush_size = 20;
            //console.log(e);

            var r = canvas.getBoundingClientRect(),
            x = Math.trunc(e.clientX - r.left),
            y = Math.trunc(e.clientY - r.top);
            //console.log(x, y);

            for (i = x-brush_size; i <= x+brush_size; i++){
                for (j = y-brush_size; j <= y+brush_size; j++){

                    var p = ctx2.getImageData(i, j, 1, 1).data;
                    var hex = "#" + ("000000" + rgbToHex(p[0], p[1], p[2])).slice(-6);
                    ctx.fillStyle = hex;
                    ctx.fillRect(i, j, 1, 1);
                }
            }

            //console.log(dots)
        });

    }

    ///READING THE ANNOTATED WHITE PIXELS ON THE ORIGINAL IMAGE
    ///INPUT: IMAGE => OUTPUT : ARRAY OF COORDINATES
    function readpixels(e){
        mousedown = false;
        console.log('reading');

        function rgbToHex(r, g, b) {
            if (r > 255 || g > 255 || b > 255)
                throw "Invalid color component";
            return ((r << 16) | (g << 8) | b).toString(16);
            }

        dots = [];
        for(i = 0; i < canvas.height; i++){
            for (j = 0; j< canvas.width; j++){
                var p = ctx.getImageData(i, j, 1, 1).data;
                if(p[0]>100 && p[1]>100 && p[2]>100){
                    dots.push(i,j);
                    // dots.push('none');
                    // dots.push('none');
                }
            }
        }
        console.log(dots);

        //submit = document.getElementById('submit');
        document.getElementById("coordinates").value=JSON.stringify(dots);
    }
   

    ///FUNCTION TO READ KEYBOARD EVENTS
    canvas.setAttribute('tabindex', 0);
    canvas.addEventListener('keypress', newline);
    
    function newline(e) {
        var keyName = e.key;

        if (keyName == 'j' || keyName == 'J'){
            console.log('j is pressed');
            //norm = !norm;
            //console.log(norm)
            brush_size = brush_size - 10
            if(brush_size <= 0){
                brush_size = 5;
            }
            console.log(brush_size);

        }

        if (keyName == 'k' || keyName == 'K'){
            console.log('k is pressed');
            //norm = !norm;
            //console.log(norm)
            brush_size = brush_size + 10
            if(brush_size >= 20){
                brush_size = 20;
            }
            console.log(brush_size);
        }

        /*if (keyName == 'u' || keyName == 'U'){
            norm = true;
            clearpath(e);
        }*/
        

        if (keyName == 'z' || keyName == 'Z'){
            console.log('z is pressed');
            norm = !norm;
            //console.log(norm)
            erase_pixels(e);

        }

        if (keyName == 's' || keyName == 'S'){
            console.log('s is pressed')
            //console.log(norm)
            readpixels(e);
        }
    }
});
