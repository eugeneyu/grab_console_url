$( document ).ready(function() {
    var clipboard = new ClipboardJS('.clipboard');
});

function copy(text) {
	const ta = document.createElement('textarea');
	ta.style.cssText = 'opacity:0; position:fixed; width:1px; height:1px; top:0; left:0;';
	ta.value = text;
	document.body.appendChild(ta);
	ta.focus();
	ta.select();
	document.execCommand('copy');
	ta.remove();
}

function shorten_url(url_long) {
	var accessToken = "";
	var params = {
        "url_long" : url_long           
    };

    chrome.identity.getProfileUserInfo(function(userInfo) {
        console.log(JSON.stringify(userInfo));
    });

	$.ajax({
        url: "https://api-ssl.bitly.com/v4/shorten",
        cache: false,
        dataType: "json",
        method: "POST",
        contentType: "application/json",
        beforeSend: function (xhr) {
            xhr.setRequestHeader("Authorization", "Bearer " + accessToken);
        },
        data: JSON.stringify(params)
    }).done(function(data) {
        //console.log(data);
        url_short = data["link"]
        document.getElementById("url_short").innerHTML = url_short;

    }).fail(function(data) {
        console.log(data);
    });
}

window.onload = function() {
	
    	var url = "https://console.cloud.google.com/compute/instancesDetail/zones/asia-southeast1-b/instances/public-kml-train-worker-gpu57-gcpsgpc-sgp-kwaidc-com?project=kwaigo-225903";
    	// use `url` here inside the callback because it's asynchronous!
    	// document.getElementById("confirm").innerHTML = url;

    	// copy the public url to clipboard
    	var url_public = url.replace("pantheon.corp", "console.cloud");
    	copy(url_public);

    	// display project id
    	var url_object = new URL(url_public);
		var project_id = url_object.searchParams.get("project");
		document.getElementById("project_id").innerHTML = project_id;

		// display shortened URL
		shorten_url(url_public);
	
};


