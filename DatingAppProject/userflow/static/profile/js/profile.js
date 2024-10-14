let circularProgress = document.querySelector(".circular-progress"),
    progressValue = document.querySelector(".progress-value");
    
let progressStartValue = 0,    
    progressEndValue = 75,    
    speed = 100;

let progress = setInterval(() => {
    progressStartValue++;

    progressValue.textContent = `${progressStartValue}%`
    circularProgress.style.background = `conic-gradient(#DD88CF ${progressStartValue * 3.6}deg, #4B164C 0deg)`

    if(progressStartValue == progressEndValue){
        clearInterval(progress);
    }    
}, speed);

// document.getElementById('profileImage').style.backgroundImage = "url('https://images.unsplash.com/photo-1574502482076-933de46e26eb?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D')";
