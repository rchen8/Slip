var NUM_SLIDES = 80;
var currentSlide = 1;
// document.getElementById("video").addEventListener("loadedmetadata", function() {
// 	this.currentTime = 1000;
// 			// this.playbackRate = 2.0;
// }, true);

document.getElementById("buttons").addEventListener("click", function(event) {
	if (event.target.id === "back_button") {
		if (currentSlide > 1) {
			currentSlide--;
			changeSlide();
		}
	} else if (event.target.id === "next_button") {
		if (currentSlide < NUM_SLIDES) {
			currentSlide++;
			changeSlide();
		}
	}
});

function changeSlide() {
	var slide = tag("img", {src: "slides/Small01-" + (currentSlide < 10 ? "0" + currentSlide : currentSlide) + ".png", height: 600}, "");
	var div = document.getElementById("slides");
	div.innerHTML = "";
	div.appendChild(slide);
}