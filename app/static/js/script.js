var NUM_SLIDES = 42;
var currentSlide = 0;

var LEFT_ARROW_KEY = 37;
var RIGHT_ARROW_KEY = 39;

$(document).on("keyup", function(event) {
  event.preventDefault();
	if (event.keyCode === LEFT_ARROW_KEY) {
    previousSlide();
  } else if (event.keyCode === RIGHT_ARROW_KEY) {
		nextSlide();
	}
});

$(".back_button").click(previousSlide);
$(".next_button").click(nextSlide);
$(".slide_button").click(changeSlide);
$(".video_button").click(changeVideo); 

function changeVideo() {
  var video = tag("video", {controls: "", height: 540}, [
    tag("source", {src: "video", type: "video/mp4"}, ""),
    "Your browser does not support the video tag."
  ]);
  var $div = $(".frame");
  $div.html("");
  $div.append(video);

  $("video").on("loadedmetadata", function(event) {
    event.preventDefault();
    this.currentTime = 1000;
    console.log(this.currentTime)
    this.play();
  });
}

function changeSlide() {
  var slide = tag("img", {src: "slide?filename=slide-" + currentSlide + ".jpg", height: 540}, "");
  var $div = $(".frame");
  $div.html("");
  $div.append(slide);
}

function previousSlide() {
  if (currentSlide > 0) {
    currentSlide--;
    changeSlide();
  }
}

function nextSlide() {
  if (currentSlide < NUM_SLIDES) {
    currentSlide++;
    changeSlide();
  }
}
