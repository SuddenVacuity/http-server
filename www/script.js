/*
This file is subject to the terms and conditions found 
by requesting "/license" or in the file "LICENSE" located 
in the server source files base directory.
*/
function randomNumber() {
	document.getElementById("number").innerHTML = Math.floor(Math.random() * 1000000);
}

function getEntryText(url) {
	myId = document.getElementById("entryId").value;
	entryText = document.getElementById("entry");
	entryText.innerHTML = "---"

	if(myId.length == 0) {
		entryText.innerHTML = "!!! You Must Enter an Entry Id !!!";
		return
	}

	urlp = url + "?" + myId;

	fetch(urlp).then(function(response) {
		if(response.ok) {
			return response.text();
		} else {
			console.log("Load failed");
			return "Unable to load data"
		}
	}).then(function(text) {
		document.getElementById("entry").innerHTML = text;
	});
}

function sendEntryText(url) {
	myId = document.getElementById("entryId").value;
	myValue = document.getElementById("entryData").value;
	entryText = document.getElementById("entry");
	entryText.innerHTML = "---"

	if(myId.length == 0) {
		entryText.innerHTML = "!!! You Must Enter an Entry Id !!!";
		return
	}

	fetch(url, {
		method: "POST",
		headers: {
			'Accept': 'application/json',
			'Content-Type': 'application/json'
		},

		body: JSON.stringify({
			'id': myId,
			'value': myValue
		})
	});

}