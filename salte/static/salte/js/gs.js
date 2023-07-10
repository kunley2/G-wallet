//document.addEventListener('DOMContentLoaded', function() {

window.onload = function() {
  var loader = document.getElementById('loader');
 
  var landingPage = document.querySelector('.landing-page');
  var timeline = gsap.timeline();

  timeline
    .fromTo(loader, { opacity: 1 }, { opacity: 0, duration: 2, delay: 1 })
    .to('.loader-content', { opacity: 0, duration: 1 }, '-=1') // Fade out the loader content
    
    .to(landingPage, { opacity: 1, duration: 1 }); // Reveal landing page
};
