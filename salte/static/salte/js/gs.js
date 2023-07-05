//document.addEventListener('DOMContentLoaded', function() {

window.onload = function() {
  var loader = document.getElementById('loader');
  var blinders = document.querySelectorAll('.blinder');
  var landingPage = document.getElementById('landing-page');
    var timeline = gsap.timeline();

    timeline
      .fromTo(loader, { opacity: 1 }, { opacity: 0, duration: 2, delay: 1 })
      .fromTo(blinders, { height: '100%' }, { height: '0%', duration: 1, stagger: 0.2 }, '-=1')
      .to(landingPage, { opacity: 1, duration: 1 });
  };
