$(document).ready(function(){

    //Parsing
    var rawData = Steps;
    stepKeys = Object.keys(Steps);
    numberOfIterations = stepKeys.length-1;
    console.log("Number of Iterations: "+ numberOfIterations);
    // for (let index = 0; index < 6; index++) {
    //     rawData[index]= Steps[index];
        
    // }
    // console.log(rawData);


    //Drawing
    var ctx = document.getElementById('grid').getContext('2d');
    var stepNumber = document.getElementById('stepNumber');
    //Square Variables
    w = 24;
    h = 24;
    side = 9;
    gap = 2;

    //Color Setups
    zeroValue = "rgb(9,6,0)";
    oneValue = "rgb(255,264,62)";
    targetValue = "rgb(255,85,62)";

    //Initialize Target
    for (var x = 0, j = 0; j < w; x+=side, j++) {
        for (var y = 0, i=0; i < h; y+=side, i++) {   
            if(target[i][j] == 0){
                ctx.fillStyle = zeroValue;
                ctx.beginPath();    
                ctx.rect (x, y, side-gap, side-gap);
                ctx.fill();
                ctx.closePath();
            }else if(target[i][j] == 1){
                ctx.fillStyle = targetValue;
                ctx.beginPath();  
                ctx.rect (x, y, side-gap, side-gap);
                ctx.fill();
                ctx.closePath();
            }                                        
        }
    }   

    //Main Loop Configuration
    delayMS = 1000;
    initalDelay = delayMS;
    delayBeforeLoop = 5000;
    currentFrame = rawData[0];
    (function mainLoop(frame) {
        setTimeout(function() {
            
            // console.log(currentFrame);
            // redValue-= 20;
            // greenValue+= 20;

            for (var x = 0, j = 0; j < w; x+=side, j++) {
                for (var y = 0, i=0; i < h; y+=side, i++) {   
                    // console.log(i,j,i%2,j%2);
                    if(currentFrame[i][j] == 0 && target[i][j] == 0){
                        ctx.fillStyle = zeroValue;
                        ctx.beginPath();    
                        ctx.rect (x, y, side-gap, side-gap);
                        ctx.fill();
                        ctx.closePath();
                    }else if(target[i][j] == 1 && currentFrame[i][j] == 0){
                        ctx.fillStyle = targetValue;
                        ctx.beginPath();  
                        ctx.rect (x, y, side-gap, side-gap);
                        ctx.fill();
                        ctx.closePath();
                    }                    
                    else if(currentFrame[i][j] == 1){
                        ctx.fillStyle = oneValue;
                        ctx.beginPath();  
                        ctx.rect (x, y, side-gap, side-gap);
                        ctx.fill();
                        ctx.closePath();
                    }                                        
                }
            }      
            // console.log("STEP #"+frame);    
            stepNumber.innerHTML = frame+1; 
          if (frame < numberOfIterations){ 
            delayMS = initalDelay;
            frame++;
            currentFrame = rawData[frame];  
            mainLoop(frame)            
          }else{
              console.log("Looping")
              delayMS = delayBeforeLoop;
              frame = 0;
              currentFrame = rawData[0];
              mainLoop(frame) 
          };   
        }, delayMS)
      })(0);     


});