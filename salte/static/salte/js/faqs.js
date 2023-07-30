window.onload = function() {
  gsap.registerPlugin(ScrollTrigger)
  var timeline = gsap.timeline({
    scrollTrigger: {
        trigger: '.accordion', 
        pin: false,
        start: '-50% center',
        end: '350% center',
        //markers: true,
        scrub: 1,
        ease: 'linear',
      }
  })

  timeline.to('.accordion .text', {
    height: 0,
    paddingBottom: 0,
    duration: 1,
    opacity: 0,
    stagger: .7,
  })
  timeline.to('.accordion', {
    marginBottom: 1,
    stagger: .7,
  }, '<')


  const lenis = new Lenis()

    lenis.on('scroll', (e) => {
      console.log(e)
    })

    function raf(time) {
      lenis.raf(time)
      requestAnimationFrame(raf)
    }

    requestAnimationFrame(raf)



}