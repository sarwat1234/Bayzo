gsap.registerPlugin(ScrollTrigger);

const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

// Starting positions for the story scene
gsap.set("#cust", { x: 60, y: 360 });
gsap.set("#mech", { x: 960, y: 360 });
gsap.set("#hood", { svgOrigin: "602 266" });
gsap.set("#custArm", { transformOrigin: "0px 0px" });
gsap.set("#helpRing", { svgOrigin: "735 120" });
gsap.set("#done", { scale: 0, svgOrigin: "440 160" });
gsap.set(".cap", { opacity: 0, y: 24 });
gsap.set("#cap1", { opacity: 1, y: 0 });

// Small looping details (smoke, question mark, help button pulse)
if (!reduce) {
  gsap.to("#qmark", { y: -8, repeat: -1, yoyo: true, duration: 0.8, ease: "sine.inOut" });
  gsap.utils.toArray("#smoke circle").forEach((c, i) => {
    gsap.fromTo(c, { y: 0, opacity: 0.6 }, { y: -60, opacity: 0, duration: 2.4, repeat: -1, delay: i * 0.8, ease: "none" });
  });
  gsap.fromTo("#helpRing", { scale: 1, opacity: 0.9 }, { scale: 1.9, opacity: 0, duration: 1.4, repeat: -1, ease: "power1.out" });

  // One opening moment for the hero
  gsap.from(".hero h1, .hero p, .hero .actions", { opacity: 0, y: 30, duration: 1, stagger: 0.15, ease: "power3.out" });
}

// The scroll story: one timeline, five scenes, each one unit long
const tl = gsap.timeline({
  defaults: { ease: "power2.inOut" },
  scrollTrigger: reduce ? null : { trigger: "#story", start: "top top", end: "+=450%", pin: true, scrub: 0.8 }
});

// Caption swaps
function step(n, t) {
  tl.to("#cap" + (n - 1), { opacity: 0, y: -24, duration: 0.25 }, t - 0.05)
    .to("#cap" + n, { opacity: 1, y: 0, duration: 0.3 }, t + 0.2);
}
step(2, 1); step(3, 2); step(4, 3); step(5, 4);

// Scene 2: tools light up, customer walks in and smiles
tl.to("#qmark, #smoke", { opacity: 0, duration: 0.3 }, 1)
  .to("#tools", { opacity: 1, duration: 0.6 }, 1)
  .to("#toolGlow", { opacity: 1, duration: 0.6 }, 1)
  .to("#cust", { x: 170, duration: 0.9 }, 1)
  .to("#mouthWorry", { opacity: 0, duration: 0.2 }, 1.4)
  .to("#mouthHappy", { opacity: 1, duration: 0.2 }, 1.4);

// Scene 3: hood opens, instruction video appears
tl.to("#hood", { rotation: -58, duration: 0.8 }, 2)
  .to("#tablet", { opacity: 1, duration: 0.5 }, 2.1);

// Scene 4: stuck, presses the help button
tl.to("#mouthHappy", { opacity: 0, duration: 0.2 }, 3)
  .to("#mouthWorry", { opacity: 1, duration: 0.2 }, 3)
  .to("#help", { opacity: 1, duration: 0.4 }, 3)
  .to("#custArm", { rotation: -165, duration: 0.5 }, 3.1)
  .to("#bubble", { opacity: 1, duration: 0.4 }, 3.3);

// Scene 5: mechanic walks over and hands the wrench, car is fixed
tl.to("#bubble, #help", { opacity: 0, duration: 0.3 }, 4)
  .to("#mech", { x: 335, duration: 0.9 }, 4)
  .to("#custArm", { rotation: -90, duration: 0.5 }, 4.3)
  .to("#mouthWorry", { opacity: 0, duration: 0.2 }, 4.5)
  .to("#mouthHappy", { opacity: 1, duration: 0.2 }, 4.5)
  .to("#wrenchM", { opacity: 0, duration: 0.2 }, 4.85)
  .to("#wrenchC", { opacity: 1, duration: 0.2 }, 4.85)
  .to("#done", { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2)" }, 4.95);

// Visitors who prefer less motion see the finished scene
if (reduce) tl.progress(1);