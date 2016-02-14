var NUM_SLIDES = 80;

document.getElementById("video").addEventListener("loadedmetadata", function() {
	this.currentTime = 1000;
			// this.playbackRate = 2.0;
}, true);

for (var i = 1; i <= NUM_SLIDES; i++) {
	var div = document.getElementById("slides");
	div.appendChild(tag("img", {src: "slides/Small01-" + (i < 10 ? "0" + i : i) + ".png", width: 1080}, ""));
}