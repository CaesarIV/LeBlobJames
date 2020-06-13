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
    var ctxArt = document.getElementById('gridArt').getContext('2d');
    var stepNumberArt = document.getElementById('stepNumberArt');
    //Square Variables
    wArt = 24;
    hArt = 24;
    sideArt = 9;
    gapArt = 0;

    //Color Setups
    zeroValue = "rgb(9,6,0)";
    oneValue = "rgb(255,264,62)";
    targetValue = "rgb(255,85,62)";

    //Initialize Target
    for (var x = 0, j = 0; j < wArt; x+=sideArt, j++) {
        for (var y = 0, i=0; i < hArt; y+=sideArt, i++) {   
            //if(i < target[0].length && j < target[0][0]){
                if(target[i][j] == 0){
                    ctxArt.fillStyle = zeroValue;
                    ctxArt.beginPath();    
                    ctxArt.rect (x, y, sideArt-gapArt, sideArt-gapArt);
                    ctxArt.fill();
                    ctxArt.closePath();
                }else if(target[i][j] == 1){
                    ctxArt.fillStyle = targetValue;
                    ctxArt.beginPath();  
                    ctxArt.rect (x, y, sideArt-gapArt, sideArt-gapArt);
                    ctxArt.fill();
                    ctxArt.closePath();
                }     
            // }else{
            //     ctxArt.fillStyle = zeroValue;
            //     ctxArt.beginPath();    
            //     ctxArt.rect (x, y, sideArt-gapArt, sideArt-gapArt);
            //     ctxArt.fill();
            //     ctxArt.closePath();
            // }                                   
        }
    }   

    //Main Loop Configuration
    delayMS = 1000;
    initalDelay = delayMS;
    delayBeforeLoop = 5000;
    currentFrameArt = rawData[0];
    (function mainLoop(frame) {
        setTimeout(function() {
            
            // console.log(currentFrameArt);
            // redValue-= 20;
            // greenValue+= 20;

            for (var x = 0, j = 0; j < wArt; x+=sideArt, j++) {
                for (var y = 0, i=0; i < hArt; y+=sideArt, i++) {   
                    // console.log(i,target[0].length);
                    //if(i < target[0].length && j < target[0][0]){
                        if(currentFrameArt[i][j] == 0 && target[i][j] == 0){
                            ctxArt.fillStyle = zeroValue;
                            ctxArt.beginPath();    
                            ctxArt.rect (x, y, sideArt-gapArt, sideArt-gapArt);
                            ctxArt.fill();
                            ctxArt.closePath();
                        }else if(target[i][j] == 1 && currentFrameArt[i][j] == 0){
                            ctxArt.fillStyle = targetValue;
                            ctxArt.beginPath();  
                            ctxArt.rect (x, y, sideArt-gapArt, sideArt-gapArt);
                            ctxArt.fill();
                            ctxArt.closePath();
                        }                    
                        else if(currentFrameArt[i][j] == 1){
                            ctxArt.fillStyle = oneValue;
                            ctxArt.beginPath();  
                            ctxArt.rect (x, y, sideArt-gapArt, sideArt-gapArt);
                            ctxArt.fill();
                            ctxArt.closePath();
                        }  
                    //}
                    // else{
                    //     ctxArt.fillStyle = zeroValue;
                    //     ctxArt.beginPath();    
                    //     ctxArt.rect (x, y, sideArt-gapArt, sideArt-gapArt);
                    //     ctxArt.fill();
                    //     ctxArt.closePath();
                    // }                                      
                }
            }      
            // console.log("STEP #"+frame);    
            stepNumberArt.innerHTML = frame+1; 
          if (frame < numberOfIterations){ 
            delayMS = initalDelay;
            frame++;
            currentFrameArt = rawData[frame];  
            mainLoop(frame)            
          }else{
              console.log("Looping")
              delayMS = delayBeforeLoop;
              frame = 0;
              currentFrameArt = rawData[0];
              mainLoop(frame) 
          };   
        }, delayMS)
      })(0);     


});