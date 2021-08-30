console.log('background page started');

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
    if (request.todo == "showPageAction"){
        chrome.tabs.query({active:true, currentWindow:true}, function(tabs){
            chrome.pageAction.show(tabs[0].id);
        });
    }
});

chrome.runtime.onMessage.addListener(function (msg, sender, sendResponse) {
    if (msg.type == 'ACTIVITY_RECOMMENDATION_READY') {
        console.log("received: " + msg.information); 
        if (msg.information) {
            sendResponse({
                type: "RECOMM_RESPONSE",
                information: "i received your information"
            });
            fetch("http://127.0.0.1:5000/data", {
                method: 'POST',
                mode: 'cors',
                headers: {
                    'Accept': 'application/json, application/xml, text/plain, text/html, *.*',
                    'Content-Type': 'application/json; charset=utf-8'
                },
                body: JSON.stringify(msg)
            })
                .then(response => response.text())
                .then(response => {
                    dictionary = JSON.parse(response);
                    console.log(dictionary)
                    keys = Object.keys(dictionary);
                    values = Object.values(dictionary);

                    sendDataToPopup(dictionary);
                })
                .catch(error => console.log('Error:', error));

        } else {
            sendResponse({
                type: "NO_DATA"
            });
        }
    }
});

function sendDataToPopup(dataFromServer) {
    chrome.runtime.sendMessage({
        message: 'DATA_FROM_SERVER',
        dataSent: dataFromServer
    });
}