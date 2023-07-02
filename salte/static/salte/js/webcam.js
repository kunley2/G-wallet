"use strict";
var video = document.getElementById('video');
var canvas = document.getElementById('canvas');
var videoStream = null;
var preLog = document.getElementById('preLog');
let photo = null
let streaming = false;
const width = 320; // We will scale the photo width to this
let height = 0

function log(text)
{
	if (preLog) preLog.textContent += ('\n' + text);
	else alert(text);
}

function snapshot()
{
    if (width && height) {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        var data = canvas.toDataURL('image/png');
        photo.setAttribute('src', data);
  } else {
    clearphoto();
  }
}

function clearphoto() {
    var context = canvas.getContext('2d');
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);
  
    var data = canvas.toDataURL('image/png');
    photo.setAttribute('src', data);
  }

function noStream()
{
	log('Access to camera was denied!');
}

function stop()
{
	var myButton = document.getElementById('buttonStop');
	if (myButton) myButton.disabled = true;
	myButton = document.getElementById('buttonSnap');
	if (myButton) myButton.disabled = true;
	if (videoStream)
	{
		if (videoStream.stop) videoStream.stop();
		else if (videoStream.msStop) videoStream.msStop();
		videoStream.onended = null;
		videoStream = null;
	}
	if (video)
	{
		video.onerror = null;
		video.pause();
		if (video.mozSrcObject)
			video.mozSrcObject = null;
		video.src = "";
	}
	myButton = document.getElementById('buttonStart');
	if (myButton) myButton.disabled = false;
}

function gotStream(stream)
{
	var myButton = document.getElementById('buttonStart');
	if (myButton) myButton.disabled = true;
	videoStream = stream;
	navigator.mediaDevices
      .getUserMedia({ video: true, audio: false })
      .then((stream) => {
        video.srcObject = stream;
        video.play();
      })
      .catch((err) => {
        console.error(`An error occurred: ${err}`);
      });

    video.addEventListener(
      "canplay",
      (ev) => {
        if (!streaming) {
          height = video.videoHeight / (video.videoWidth / width);

          // Firefox currently has a bug where the height can't be read from
          // the video, so we will make assumptions if this happens.

          if (isNaN(height)) {
            height = width / (4 / 3);
          }

          video.setAttribute("width", width);
          video.setAttribute("height", height);
          canvas.setAttribute("width", width);
          canvas.setAttribute("height", height);
          streaming = true;
        }
      },
      false
    );

    myButton.addEventListener(
      "click",
      (ev) => {
        snapshot();
        ev.preventDefault();
      },
      false
    );

    clearphoto();
  console.log('outside the function')
	myButton = document.getElementById('buttonSnap');
	if (myButton) {console.log('in the buttonSnap'); myButton.disabled = false;}
	myButton = document.getElementById('buttonStop');
	if (myButton) {myButton.disabled = false;}
}

function start()
{
  photo = document.getElementById("photo")
	if ((typeof window === 'undefined') || (typeof navigator === 'undefined')) log('This page needs a Web browser with the objects window.* and navigator.*!');
	else if (!(video && canvas)) log('HTML context error!');
	else
	{
		log('Get user media…');
		if (navigator.getUserMedia) navigator.getUserMedia({video:true}, gotStream, noStream);
		else if (navigator.oGetUserMedia) navigator.oGetUserMedia({video:true}, gotStream, noStream);
		else if (navigator.mozGetUserMedia) navigator.mozGetUserMedia({video:true}, gotStream, noStream);
		else if (navigator.webkitGetUserMedia) navigator.webkitGetUserMedia({video:true}, gotStream, noStream);
		else if (navigator.msGetUserMedia) navigator.msGetUserMedia({video:true, audio:false}, gotStream, noStream);
		else log('getUserMedia() not available from your Web browser!');
	}
}

// start();