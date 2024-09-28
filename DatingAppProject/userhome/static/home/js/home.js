//story section
let currentScrollPosition = 0;
let scrollAmount = 320;
const sCont = document.querySelector(".story-container");
const hScroll = document.querySelector(".horizontal-scroll");
const btnScrollLeft = document.querySelector("#btn-scroll-left");
const btnScrollRight = document.querySelector("#btn-scroll-right");
btnScrollLeft.style.opacity = 0;
// alert("sCont.offsetWidth:=",sCont.offsetWidth);
// alert("hScroll.offsetWidth:=",hScroll.offsetWidth);
let maxScroll = -sCont.offsetWidth + hScroll.offsetWidth; //-612

function scrollHorizontally(val){
  currentScrollPosition += (val * scrollAmount);
  
  sCont.style.left = currentScrollPosition + "px";//-320
  // alert(currentScrollPosition);
  // alert(sCont.style.left );//-612
  // alert(maxScroll);

  if(currentScrollPosition >= 0){
    currentScrollPosition = 0;
    btnScrollLeft.style.opacity = 0;
  }else{
    btnScrollLeft.style.opacity = 1;
  }

  if(currentScrollPosition <= maxScroll){
    currentScrollPosition = maxScroll;
    btnScrollRight.style.opacity = 0;
  }else{
    btnScrollRight.style.opacity = 1;
  }
}


document.addEventListener('DOMContentLoaded', function() {
  // Select all tabs and sections
  const tabs = document.querySelectorAll('.options-list-items');
  const sections = document.querySelectorAll('.profile-view');

  // Add event listeners to each tab
  tabs.forEach(tab => {
      tab.addEventListener('click', function(event) {
          event.preventDefault();

          // Remove 'active' class from all tabs and 'd-none' class from all sections
          tabs.forEach(t => t.classList.remove('active'));
          sections.forEach(s => s.classList.add('d-none'));

          // Add 'active' class to the clicked tab
          tab.classList.add('active');

          // Show the section related to the clicked tab
          const targetId = tab.id.replace('-tab', '');
          const targetSection = document.getElementById(targetId);
          if (targetSection) {
              targetSection.classList.remove('d-none');
          }
      });
  });

  // Set the default active tab and section
  const defaultTab = document.getElementById('location-tab');
  if (defaultTab) {
      defaultTab.click();
  }
});
