// var NUM_SLIDES = 80;
// var currentSlide = 1;

// var times = [20.654933, 29.029967, 70.404633, 108.2758, 218.1856, 227.9954, 237.471533, 258.626, 294.662, 394.428333, 485.919733, 494.2614, 502.603067, 540.240667, 644.778433, 678.1451, 710.744333, 808.341833, 836.836967, 905.905967, 924.424467, 979.579567, 1017.617567, 1078.878767, 1112.245433, 1131.8984, 1249.882933, 1258.2246, 1261.494533, 1334.0003, 1413.746633, 1589.3554, 1604.003367, 1645.7117, 1673.1391, 1759.191733, 1776.509033, 1808.607767, 1829.9958, 1914.847233, 1929.5953, 2005.304267, 2038.771033, 2068.3339, 2093.3589, 2126.725567, 2188.3538, 2212.511267, 2301.3667, 2385.2505, 2484.2494, 2542.240667, 2936.6013, 2953.584933, 3047.412, 3138.6031, 3188.286067, 3204.9694, 3209.1736, 3245.4098, 3463.3275, 3532.5967, 3637.568233, 3662.593233, 3692.389667, 3817.3812, 3875.772867, 3884.114533, 4071.568467, 4211.408167, 4236.433167, 4260.0234, 4276.806833, 4351.381333, 4426.923467, 4463.259767, 4500.396867, 4543.907, 4599.228933, 4604.133833];

// document.addEventListener("keyup", function(event) {
// 	if (event.keyCode === 39) {
// 		if (currentSlide < NUM_SLIDES) {
// 			currentSlide++;
// 			changeSlide();
// 		}
// 	} else if (event.keyCode === 37) {
// 		if (currentSlide > 1) {
// 			currentSlide--;
// 			changeSlide();
// 		}
// 	}
// });

// document.getElementById("button").addEventListener("click", function(event) {
// 	if (event.target.id === "back_button") {
// 		if (currentSlide > 0) {
// 			currentSlide--;
// 			changeSlide();
// 		}
// 	} else if (event.target.id === "next_button") {
// 		if (currentSlide < NUM_SLIDES - 1) {
// 			currentSlide++;
// 			changeSlide();
// 		}
// 	} else if (event.target.id === "video_button") {
// 		changeVideo(times[currentSlide]);
// 	} else if (event.target.id === "slide_button") {
// 		changeSlide();
// 	}
// });

// function changeSlide() {
// 	var slide = tag("img", {src: "slides/a-" + currentSlide + ".jpg", height: 540}, "");
// 	var div = document.getElementById("frame");
// 	div.innerHTML = "";
// 	div.appendChild(slide);

// 	document.getElementById("slide_button").setAttribute("id", "video_button");
// 	document.getElementById("video_button").setAttribute("src", "images/video_button.png");
// }

// function changeVideo(time) {
// 	var div = document.getElementById("frame");
// 	var video = tag("video", {controls:"", height: 540}, [
// 		tag("source", {src: "160106-cs103-540.mp4", type: "video/mp4"}, ""),
// 		"Your browser does not support the video tag."
// 	]);

// 	video.addEventListener("loadedmetadata", function(event) {
// 		this.currentTime = time;
// 	})

// 	div.innerHTML = "";
// 	div.appendChild(video);

// 	document.getElementById("video_button").setAttribute("id", "slide_button");
// 	document.getElementById("slide_button").setAttribute("src", "images/slide_button.png");
// }

// // $.ajax({ url: 'http://localhost:5000/', success: function(response) {
// //  		console.log(response); 
// // 	}
// // });

// // $("#form").submit(function(event) {
// // 	event.preventDefault();
// // 	var fd = new FormData();
// // 	fd.append('file', $('input[type=file]')[0].files[0]);
// // 	// fd.append('file2', $('input[type=file]')[0].files[0]);
// // 	$.ajax({
// // 	  url: 'http://localhost:5000/', 
// // 	  type: 'POST',
// // 	  data: fd, // The form with the file inputs.
// // 	  processData: false,
// // 	  contentType: false                          // Using FormData, no need to process data.
// // 	}).done(function(data) {
// // 	  console.log(data);
// // 	}).fail(function(){
// // 	  console.log("An error occurred, the files couldn't be sent!");
// // 	});
// // });