var NUM_SLIDES = 80;
var currentSlide = 1;

document.addEventListener("keyup", function(event) {
	if (event.keyCode === 39) {
		if (currentSlide < NUM_SLIDES) {
			currentSlide++;
			changeSlide();
		}
	} else if (event.keyCode === 37) {
		if (currentSlide > 1) {
			currentSlide--;
			changeSlide();
		}
	}
});

document.getElementById("button").addEventListener("click", function(event) {
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
	} else if (event.target.id === "video_button") {
		changeVideo(1000);
	} else if (event.target.id === "slide_button") {
		changeSlide();
	}
});

function changeSlide() {
	var slide = tag("img", {src: "slides/Small01-" + (currentSlide < 10 ? "0" + currentSlide : currentSlide) + ".png", height: 540}, "");
	var div = document.getElementById("frame");
	div.innerHTML = "";
	div.appendChild(slide);

	document.getElementById("slide_button").setAttribute("id", "video_button");
	document.getElementById("video_button").setAttribute("src", "images/video_button.png");
}

function changeVideo(time) {
	var div = document.getElementById("frame");
	var video = tag("video", {controls:"", height: 540}, [
		tag("source", {src: "videos/lecture.mp4", type: "video/mp4"}, ""),
		"Your browser does not support the video tag."
	]);

	video.addEventListener("loadedmetadata", function(event) {
		this.currentTime = time;
	})

	div.innerHTML = "";
	div.appendChild(video);

	document.getElementById("video_button").setAttribute("id", "slide_button");
	document.getElementById("slide_button").setAttribute("src", "images/slide_button.png");
}

// document.getElementById("test").addEventListener("click", function(event) {
// 	$.ajax( {
// 		url: "test.py",
// 		success: function(response) {
// 			console.log("python works");
// 		}
// 	});
// });

function test() {
	var file = document.getElementById("file").files;
	for (var i = 0; i < file.length; i++) {
		console.log(file[i]);
	}
}