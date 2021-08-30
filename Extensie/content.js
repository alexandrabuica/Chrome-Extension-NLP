function getArticleBodyRomaniaLibera(){
    var text = ""
    var articleOpening = document.getElementsByClassName('font-bold text-xl');
    text += articleOpening[0].innerText;
    var paragraphs = document.getElementById('rl-article-content').getElementsByTagName('p');
    for (para of paragraphs) {
        text += para.innerText;
    }
    return text;
}

function getArticleBodyGandul(){
    var text = ""
    var articleOpening = document.getElementsByClassName('single__content')[0].getElementsByTagName('strong');
    for (op of articleOpening){
        text += op.innerText;
    }  
    var paragraphs = document.getElementsByClassName('single__content')[0].getElementsByTagName('p');
    for (para of paragraphs) {
        text += para.innerText;
    }
    return text;
}

function getArticleBodyLibertatea() {
    var text = ""
    var articleOpening = document.getElementsByClassName('intro');
    text += articleOpening[0].innerText;
    var paragraphs = document.getElementsByClassName('article-body js-copy-text')[0].getElementsByTagName('p');
    for (para of paragraphs) {
        text += para.innerText;
    }
    return text;
}

function getArticleBodyJurnalul() {
    var text = ""
    var paragraphs = document.getElementsByClassName('text')[0].getElementsByTagName('p');
    for (para of paragraphs) {
        text += para.innerText;
    }
    return text;
}

function getArticleTitle(){
    var title = ""
    title = document.getElementsByTagName('h1')[0].innerHTML;
    return title.trim();
}
 

chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        console.log(request.message);
        if (request.message === "startRomania") {
            sendMessageToBackgroundScriptRomania(request.sentiment); 
        }
        if (request.message === "startLib") {
            sendMessageToBackgroundScriptLib(request.sentiment);
        }
        if (request.message === "startGandul"){
            sendMessageToBackgroundScriptGandul(request.sentiment);
        }
        if (request.message === "startJurnalul"){
            sendMessageToBackgroundScriptJurnalul(request.sentiment);
        }
    }
);

function sendMessageToBackgroundScriptAdev(sent) {
    chrome.runtime.sendMessage({
        type: 'ACTIVITY_RECOMMENDATION_READY',
        information: getArticleBodyAdevarul(),
        sentiment: sent
    },
        function (response) {
            console.log(">>>>Response: ", response);
            if (response.type == 'RECOMM_RESPONSE') {
                console.log(response.information);
            }
        });
}

function sendMessageToBackgroundScriptRomania(sent) {
    chrome.runtime.sendMessage({
        type: 'ACTIVITY_RECOMMENDATION_READY',
        information: getArticleBodyRomaniaLibera(),
        title: getArticleTitle(),
        sentiment: sent
    },
        function (response) {
            console.log(">>>>Response: ", response);
            if (response.type == 'RECOMM_RESPONSE') {
                console.log(response.information);
            }
        });
}

function sendMessageToBackgroundScriptGandul(sent) {
    chrome.runtime.sendMessage({
        type: 'ACTIVITY_RECOMMENDATION_READY',
        information: getArticleBodyGandul(),
        title: getArticleTitle(),
        sentiment: sent
    },
        function (response) {
            console.log(">>>>Response: ", response);
            if (response.type == 'RECOMM_RESPONSE') {
                console.log(response.information);
            }
        });
}

function sendMessageToBackgroundScriptLib(sent) {
    chrome.runtime.sendMessage({
        type: 'ACTIVITY_RECOMMENDATION_READY',
        information: getArticleBodyLibertatea(),
        title: getArticleTitle(),
        sentiment: sent
    },
        function (response) {
            console.log(">>>>Response: ", response);
            if (response.type == 'RECOMM_RESPONSE') {
                console.log(response.information);
            }
        });
}

function sendMessageToBackgroundScriptJurnalul(sent) {
    chrome.runtime.sendMessage({
        type: 'ACTIVITY_RECOMMENDATION_READY',
        information: getArticleBodyJurnalul(),
        title: getArticleTitle(),
        sentiment: sent
    },
        function (response) {
            console.log(">>>>Response: ", response);
            if (response.type == 'RECOMM_RESPONSE') {
                console.log(response.information);
            }
        });
}

chrome.runtime.sendMessage({todo:"showPageAction"});