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

// $.ajax({ url: 'http://localhost:5000/', success: function(response) {
//  		console.log(response); 
// 	}
// });

$("#form").submit(function(event) {
	event.preventDefault();
	var fd = new FormData();
	fd.append('file', $('input[type=file]')[0].files[0]);
	$.ajax({
	  url: 'http://localhost:5000/', 
	  type: 'POST',
	  data: fd, // The form with the file inputs.
	  processData: false,
	  contentType:false                          // Using FormData, no need to process data.
	}).done(function(data) {
	  console.log(data);
	}).fail(function(){
	  console.log("An error occurred, the files couldn't be sent!");
	});
});

