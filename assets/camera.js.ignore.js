/**
 * @license
 * Copyright 2019 Google LLC. All Rights Reserved.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * =============================================================================
 */
const videoWidth = 150;
const videoHeight = 100;

const defaultFrameRate = 10;
const defaultFrameCacheSize = 10;

const defaultInfoDivId = 'info';
const defaultInputVideoId = 'user-video';
const defaultPoseStorageId = 'cachePoses';

const defaultAlgorithm = 'single-pose'
const defaultArchitecture = 'MobileNetV1'

const defaultQuantBytes = 4;
const defaultMobileNetMultiplier = 0.75;
const defaultMobileNetStride = 16;
const defaultMobileNetInputResolution = 300;


/**
 * =============================================================================
 * Loads a the camera to be used in the demo
 *
 */
function isAndroid() {
  return /Android/i.test(navigator.userAgent);
}

function isiOS() {
  return /iPhone|iPad|iPod/i.test(navigator.userAgent);
}

function isMobile() {
  return isAndroid() || isiOS();
}
 
async function setupCamera() {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
    throw new Error(
        'Browser API navigator.mediaDevices.getUserMedia not available');
  }

  const video = document.getElementById(defaultInputVideoId);
  video.width = videoWidth;
  video.height = videoHeight;

  const mobile = isMobile();
  const stream = await navigator.mediaDevices.getUserMedia({
    'audio': false,
    'video': {
      facingMode: 'user',
      width: mobile ? undefined : videoWidth,
      height: mobile ? undefined : videoHeight
    },
  });
  video.srcObject = stream;

  return new Promise((resolve) => {
    video.onloadedmetadata = () => {
      resolve(video);
    };
  });
}

async function loadVideo() {
  const video = await setupCamera();
  video.play();

  return video;
}


/**
 * =============================================================================
 * Feeds an image to posenet to estimate poses - this is where the magic
 * happens. This function loops with a requestAnimationFrame method.
 */
function detectPoseInFrame(video, posemodel) {

  // storage for poses
  sessionStorage.setItem(defaultPoseStorageId, JSON.stringify([]));

  async function poseDetectionFrame() {

  	// this function caches the last N keypoints in the browser
	function addLatestPose(x) {
      let cachePoses = JSON.parse(sessionStorage.getItem(defaultPoseStorageId));
      cachePoses.push(x);

      let latestCachePoses = cachePoses.slice(-defaultFrameCacheSize);
      sessionStorage.setItem(defaultPoseStorageId, JSON.stringify(latestCachePoses));
  	}

	const pose = await posemodel.estimateSinglePose(video, {
      flipHorizontal: true
	});

    // this function dynamically adjusts the interval
    // requestAnimationFrame(poseDetectionFrame)
    setTimeout(function() {
      requestAnimationFrame(poseDetectionFrame)
      addLatestPose(pose)
    }, 1000 / defaultFrameRate);


  }
  	
  poseDetectionFrame();

}


/**
 * =============================================================================
 * Kicks off the demo by loading the posenet model, finding and loading
 * available camera devices, and setting off the detectPoseInRealTime function.
 */ 
async function bindPage() {

  // load Pose Estimation model to browser
  const net = await posenet.load({
    architecture: defaultArchitecture,
    outputStride: defaultMobileNetStride,
    inputResolution: defaultMobileNetInputResolution,
    multiplier: defaultMobileNetMultiplier,
    quantBytes: defaultQuantBytes
  });

  // test video capability
  let video;
  try {
    video = await loadVideo();
    let placeholder = document.getElementById('placeholder-video');
    placeholder.style.display = 'none';
  } catch (e) {
    let info = document.getElementById(defaultInfoDivId);
    info.textContent = 'this browser does not support video capture,' +
        'or this device does not have a camera';
    info.style.display = 'block';
    throw e;
  }

  // log poses per frame
  detectPoseInFrame(video, net);

/**
 * =============================================================================
 * Sends keypoint data in real-time to python API for analysis
 */ 
//   fetch('http://localhost:5000/inchworm',
//   {
//     method: 'post',
//     headers: {
//       'Accept': 'application/json, text/plain',
//       'Content-Type': 'application/json'
//     },
//     body: JSON.stringify(sessionStorage.getItem(defaultPoseStorageId))
//   })
//     .then((response) => {
// 	  return response.json();
//     })
//     .then((data) => {
// 	  console.log(data);
//     });
// 
}

navigator.getUserMedia = navigator.getUserMedia ||
    navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
// kick off the demo
bindPage();
