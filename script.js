var NUM_SLIDES = 80;
var currentSlide = 1;

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
	} else if (event.target.id === "show_video") {
		changeVideo();
	}
});

function changeSlide() {
	var slide = tag("img", {src: "slides/Small01-" + (currentSlide < 10 ? "0" + currentSlide : currentSlide) + ".png", height: 600}, "");
	var div = document.getElementById("slides");
	div.innerHTML = "";
	div.appendChild(slide);
}

function changeVideo() {
	var div = document.getElementById("slides");
	var video = tag("video", {controls:"", height: 600}, [
		tag("source", {src: "videos/lecture.mp4", type: "video/mp4"}, ""),
		"Your browser does not support the video tag."
	]);

	video.addEventListener("loadedmetadata", function(event) {
		this.currentTime = 1000;
	})

	div.innerHTML = "";
	div.appendChild(video);
}