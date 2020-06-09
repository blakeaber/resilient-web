
// AWS Credentials
AWS.config.region = 'us-east-1';
AWS.config.credentials = new AWS.CognitoIdentityCredentials({
    IdentityPoolId: 'us-east-1:8b110ca3-b5d0-478f-8df8-e864d62807f2'
});
AWS.config.credentials.get(function(err) {
    if (err) {
        alert(err);
    } else {
        console.log(AWS.config.credentials);
    }
});


// Bucket information
var bucketName = 'resilient-ai';

var bucket = new AWS.S3({
    params: {
        Bucket: bucketName
    }
});


// set global variables
var recorder;


// File format for S3 transport
function dataURLtoFile(dataurl, filename) {
    var arr = dataurl.split(','), 
        mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(btoa(arr[1])),
        n = bstr.length, 
        u8arr = new Uint8Array(n);
    while(n--){
        u8arr[n] = bstr.charCodeAt(n);
    }
    return new File([u8arr], filename, {type:mime});
}


// Events on clicking start button
function clickStartButton(is_active) {
    if (is_active) {
		var video = document.getElementById('feedback-video');

		// Disable start recording button
		document.getElementById('btn-start-recording').disabled = true;

		// Request access to the media devices
		navigator.mediaDevices.getUserMedia({
			audio: true, 
			video: true
		}).then(function(stream) {
			// Display a live preview on the video element of the page
			setSrcObject(stream, video);
			// Start to display the preview on the video element
			// and mute the video to disable the echo issue !
			video.play();
			video.muted = true;
			recorder = new RecordRTCPromisesHandler(stream, {
				mimeType: 'video/mp4'
			});
			// Start recording the video
			recorder.startRecording().then(function() {
				console.info('Recording video ...');
			}).catch(function(error) {
				console.error('Cannot start video recording: ', error);
			});
			// release stream on stopRecording
			recorder.stream = stream;
			// Enable stop recording button
			document.getElementById('btn-stop-recording').disabled = false;
		}).catch(function(error) {
			console.error("Cannot access media devices: ", error);
		});
	}
}


// Events on clicking stop button
function clickStopButton(is_active, user_data, exercise_id) {
    if (is_active) {
		var video = document.getElementById('feedback-video');
		var percentage = document.getElementById('percentage');

        let current_time = Date.now()
        let user_hash = user_data['user-hash']
        console.log(user_data)

		// Re-enable start recording button
		document.getElementById('btn-stop-recording').disabled = true;
		document.getElementById('btn-start-recording').disabled = false;

		recorder.stopRecording().then(function(){
			var Blob = recorder.getBlob();
			Blob.then(function(data){
				// When and if the promise resolving successful
				var reader = new FileReader();
				reader.onload = function() {
					var random = Math.random();
		
					// for DYNAMIC mime type based on blob
					// var objKey = 'video/user/web/'+random+'.'+data.type.split('/')[1];
		
					// otherwise...
                    var objKey = `video/user/web/${user_hash}-${exercise_id}-${current_time}.webm`;
		
					var params = {
						Key: objKey,
						ContentType: data.type,
						Body: reader.result,
						ACL: 'public-read'
					};
					var request = bucket.putObject(params);
					request.on('httpUploadProgress', function (progress) {
						percentage.innerHTML = parseInt((progress.loaded * 100) / progress.total)+'%'; 
						console.log("Uploaded :: " + parseInt((progress.loaded * 100) / progress.total)+'%');
						// console.log(progress.loaded + " of " + progress.total + " bytes");
					}).send(function(err, data){
						percentage.innerHTML = "We've securely stored your results!";
					});
				};
				reader.readAsArrayBuffer(data);
			}).catch(function(err){
				console.error(err);
			});
		});
		recorder.stream.stop();
		video.pause();
	}
}


window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
		click_start_button: clickStartButton,
		click_stop_button: clickStopButton
    }
});
