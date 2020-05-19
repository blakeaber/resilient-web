
const defaultFrameRate = 20;
const defaultFrameCacheSize = 10;
const minPoseConfidence = 0.25;

const defaultInputVideoId = 'demo-video';
const defaultOutputCanvasId = 'demo-output';
const defaultPoseStorageId = 'cachePoses';

const defaultAlgorithm = 'single-pose'
const defaultArchitecture = 'MobileNetV1'

const defaultQuantBytes = 4;
const defaultMobileNetMultiplier = 0.75;
const defaultMobileNetStride = 16;
const defaultMobileNetInputResolution = 300;


function drawPoint(ctx, y, x, r, color) {
  ctx.beginPath();
  ctx.arc(x, y, r, 0, 2 * Math.PI);
  ctx.fillStyle = color;
  ctx.fill();
}


function drawSegment([ay, ax], [by, bx], color, scale, ctx) {
  ctx.beginPath();
  ctx.moveTo(ax * scale, ay * scale);
  ctx.lineTo(bx * scale, by * scale);
  ctx.lineWidth = 2;
  ctx.strokeStyle = color;
  ctx.stroke();
}


function drawSkeleton(keypoints, minConfidence, ctx, scale = 1) {
  const adjacentKeyPoints =
      posenet.getAdjacentKeyPoints(keypoints, minConfidence);

  function toTuple({y, x}) {
    return [y, x];
  }

  adjacentKeyPoints.forEach((keypoints) => {
    drawSegment(
        toTuple(keypoints[0].position), toTuple(keypoints[1].position), 'aqua',
        scale, ctx);
  });
}


function drawKeypoints(keypoints, minConfidence, ctx, scale = 1) {
  for (let i = 0; i < keypoints.length; i++) {
    const keypoint = keypoints[i];

    if (keypoint.score < minConfidence) {
      continue;
    }

    const {y, x} = keypoint.position;
    drawPoint(ctx, y * scale, x * scale, 3, 'red');
  }
}


function detectPoseInFrame(video, posemodel) {

  const canvas = document.getElementById(defaultOutputCanvasId);
  const ctx = canvas.getContext('2d');
  const flipPoseHorizontal = true;
  
  canvas.width = video.width;
  canvas.height = video.height;

  sessionStorage.setItem(defaultPoseStorageId, JSON.stringify([]));
  async function poseDetectionFrame() {

	function addLatestPose(x) {
      let cachePoses = JSON.parse(sessionStorage.getItem(defaultPoseStorageId));
      cachePoses.push(x);

      let latestCachePoses = cachePoses.slice(-defaultFrameCacheSize);
      sessionStorage.setItem(defaultPoseStorageId, JSON.stringify(latestCachePoses));
  	}

	const pose = await posemodel.estimateSinglePose(video, {
      flipHorizontal: true
	});

    ctx.clearRect(0, 0, videoWidth, videoHeight);

    if (guiState.output.showVideo) {
      ctx.save();
      ctx.scale(-1, 1);
      ctx.translate(-videoWidth, 0);
      ctx.drawImage(video, 0, 0, videoWidth, videoHeight);
      ctx.restore();
    }

    let poses = [pose]
    poses.forEach(({score, keypoints}) => {
      if (score >= minPoseConfidence) {
        drawKeypoints(keypoints, minPartConfidence, ctx);
        drawSkeleton(keypoints, minPartConfidence, ctx);
      }
    });

    setTimeout(function() {
      requestAnimationFrame(poseDetectionFrame)
      addLatestPose(pose)
    }, 1000 / defaultFrameRate);

  }
  	
  poseDetectionFrame();

}

document.getElementById('demo-start-recording').addEventListener("click", function(){
    console.log('Start button clicked!')

    const net = await posenet.load({
        architecture: defaultArchitecture,
        outputStride: defaultMobileNetStride,
        inputResolution: defaultMobileNetInputResolution,
        multiplier: defaultMobileNetMultiplier,
        quantBytes: defaultQuantBytes
    });

    console.log('posenet model loaded!')

    var video = document.getElementById(defaultInputVideoId);

	// Disable start recording button
	document.getElementById('demo-start-recording').disabled = true;

	// Request access to the media devices
	navigator.mediaDevices.getUserMedia({
		audio: true, 
		video: true
	}).then(function(stream) {
		// Display a live preview on the video element of the page
		setSrcObject(stream, video);
		console.log('video streaming!')
		// Start to display the preview on the video element
		// and mute the video to disable the echo issue !
		video.play();
		video.muted = true;
		document.getElementById('demo-stop-recording').disabled = false;
	}).catch(function(error) {
		console.error("Cannot access media devices: ", error);
	});

    detectPoseInFrame(video, net);
}


// Events on clicking stop button
document.getElementById('demo-stop-recording').addEventListener("click", function(){
    console.log('Start button clicked!')

	var video = document.getElementById('demo-video');

	document.getElementById('demo-stop-recording').disabled = true;
	document.getElementById('demo-start-recording').disabled = false;
	video.pause();
	}
}

