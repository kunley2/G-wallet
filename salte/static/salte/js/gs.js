//document.addEventListener('DOMContentLoaded', function() {

window.onload = function() {
  var loader = document.getElementById('loader');
  var landingPage = document.querySelector('.landing-page');
  var timeline = gsap.timeline();

  timeline
    .fromTo(loader, { opacity: 1 }, { opacity: 0, duration: 2, delay: 1 })
    .to('.loader-content', { opacity: 0, duration: 1 }, '-=1') // Fade out the loader content
    .to(landingPage, { opacity: 1, duration: 1 }) // Reveal landing page
    .to('.hero-text', { duration: 1.4, y: 0, stagger: 0.1, ease: "power2" }, "-=1")
    .to('.tagline', { opacity: 1, duration: 1, delay: 0.1 }) // Fade in the tagline
    .from('.tagline', { width: 0, duration: 5, ease: "power2"}); // Typing effect on the tagline
};
