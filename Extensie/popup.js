function requestRecommendations(event) {
    chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
        var activeTab = tabs[0];
        console.log(activeTab.url)
        if (activeTab.url.includes('gandul')) {
            chrome.tabs.sendMessage(activeTab.id, { message: "startGandul", sentiment: getSentiment() });
        }

        if (activeTab.url.includes('libertatea')) {
            chrome.tabs.sendMessage(activeTab.id, { message: "startLib", sentiment: getSentiment() });
        }

        if (activeTab.url.includes('romanialibera')) {
            chrome.tabs.sendMessage(activeTab.id, { message: "startRomania", sentiment: getSentiment() });
        }

        if (activeTab.url.includes('jurnalul')) {
            chrome.tabs.sendMessage(activeTab.id, { message: "startJurnalul", sentiment: getSentiment() });
        }
    });
    document.getElementsByClassName('container-fluid')[0].style.display = 'none';
    document.getElementById("loading1").style.display = "flex";
    document.getElementById("jmb").style.display = "none";
    document.getElementById("jmb0").style.display = "none";
    document.getElementById("none").style.display = "none";
    document.getElementById("btnrecomm").style.display = "none";
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("jmb").style.display = "flex";
    document.getElementById("filter").style.display = "none";
    document.getElementById("jmb0").style.display = "flex";
    document.getElementById("loading1").style.display = "none";
    document.getElementById("btnrecomm").addEventListener("click", requestRecommendations);

});

var posRec = 0;
var negRec = 0;
chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        if (request.message === "DATA_FROM_SERVER") {
            if (request.dataSent.toString().localeCompare("none") == 0) {
                document.getElementById("loading1").style.display = "none";
                document.getElementById("btnrecomm").style.display = "none";
                document.getElementById("jmb").style.display = "flex";
                document.getElementById("jmb").innerHTML = "Hmm... nu am găsit nicio știre potrivită. Încearcă pe alt articol.";
            } else {
                arr = request.dataSent 
                console.log(arr)
                createRecCards(arr); 
                if (posRec > 0 && negRec > 0) {
                    //1 pozitive, 0 negative
                    var filtered_pos = [];
                    var filtered_neg = [];
                    for (var i = 0; i < arr.length; i++) {
                        if (arr[i].label == 0) {
                            filtered_neg.push(arr[i]);
                        } else {
                            filtered_pos.push(arr[i]);
                        }
                    } 
                    document.getElementById("filter").style.display = "flex";
                    switches = document.getElementsByClassName('form-check form-switch');
                    document.getElementById("tog1").addEventListener('change', function () {
                        var posIsChecked = document.getElementById("tog1").checked;
                        var negIsChecked = document.getElementById("tog2").checked;
                        if (posIsChecked==false){
                            negIsChecked=true;
                        }else{
                            negIsChecked=false;
                        } 
                        console.log('poz ' + posIsChecked + ' ' + 'neg ' + negIsChecked)
                        if (posIsChecked) {
                            document.getElementById("ctr").innerHTML = '';
                            createRecCards(filtered_pos);
                        } else {
                            document.getElementById("ctr").innerHTML = '';
                            createRecCards(arr);
                            negIsChecked=false;
                        }
                        document.getElementById("tog1").checked = posIsChecked;
                        document.getElementById("tog2").checked = negIsChecked;
                    });
                    document.getElementById("tog2").addEventListener('change', function () {
                        var posIsChecked = document.getElementById("tog1").checked;
                        var negIsChecked = document.getElementById("tog2").checked;
                        if (negIsChecked==false){
                            posIsChecked=true;
                        }else{
                            posIsChecked=false;
                        } 
                        console.log('poz ' + posIsChecked + ' ' + 'neg ' + negIsChecked)
                        if (negIsChecked) {
                            document.getElementById("ctr").innerHTML = '';
                            createRecCards(filtered_neg);
                        } else {
                            document.getElementById("ctr").innerHTML = '';
                            createRecCards(arr);
                            posIsChecked=false;
                        }
                        document.getElementById("tog1").checked = posIsChecked;
                        document.getElementById("tog2").checked = negIsChecked;
                    });
                }
                document.getElementById("loading1").style.display = "none";
                document.getElementById("btnrecomm").style.display = "none";
                document.getElementsByClassName('container-fluid')[0].style.display = 'block';
            }
        }
    }
);

function getSentiment() {
    var radios = document.getElementsByName('sentiment');
    for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {

            return (radios[i].value);

            break;
        }
    }
}

function createRecCards(arrayFromServer) {
    for (var i = 0; i < arrayFromServer.length; i++) {
        textToDisplay = '';
        for (var j = 0; j < arrayFromServer[i].relevant_words.length; j++) {
            elm = " #" + arrayFromServer[i].relevant_words[j] + "   ";
            textToDisplay += elm;
        }
        newsSource = ''
        if (arrayFromServer[i].source.includes('gandul')) {
            newsSource = "Sursa: Gândul"
        }
        if (arrayFromServer[i].source.includes('libertatea')) {
            newsSource = "Sursa: Libertatea"
        }
        if (arrayFromServer[i].source.includes('jurnalul')) {
            newsSource = "Sursa: Jurnalul Național"
        }
        if (arrayFromServer[i].source.includes('romanialibera')) {
            newsSource = "Sursa: România Liberă"
        }
        sentLabel = ''
        if (arrayFromServer[i].label == 'positive' || arrayFromServer[i].label == '1') {
            sentLabel = "Pozitiva";
        }
        if (arrayFromServer[i].label == 'negative' || arrayFromServer[i].label == '0') {
            sentLabel = "Negativa";
        }
        if (sentLabel == 'Pozitiva') {
            posRec++;
            var myPanel = $('<div id="div"' + i + 'class="card" style="width: 20rem;"><img src="' + arrayFromServer[i].image + '" class="card-img-top" alt="..." id="image"' + i +
                '><div class="card-body "><h5 class="card-title" id="title"' + i + '>' + arrayFromServer[i].title + '</h5><p class="card-text" style="font-weight:bold; background-color:#82E0AA; display: inline;" id="label"' + i +
                '>' + sentLabel + '</p><p class="card-text" id="relwords"' + i + '>' + textToDisplay + '</p><a href="' + arr[i].source + '" target="_blank" class="btn btn-outline-primary" id="link"' + i +
                '>Vezi articol</a></div><p id="source"' + i + 'class="newsSource" style=" font-size: 12px; font-weight: bold; margin-left:20px;">' + newsSource + '</p></div>');
        } else {
            negRec++;
            var myPanel = $('<div id="div"' + i + 'class="card" style="width: 20rem;"><img src="' + arrayFromServer[i].image + '" class="card-img-top" alt="..." id="image"' + i +
                '><div class="card-body"><h5 class="card-title" id="title"' + i + '>' + arrayFromServer[i].title + '</h5><p class="card-text" style="font-weight:bold; background-color:#EC7063; display: inline;" id="label"' + i +
                '>' + sentLabel + '</p><p class="card-text" id="relwords"' + i + '>' + textToDisplay + '</p><a href="' + arr[i].source + '" target="_blank" class="btn btn-outline-primary" id="link"' + i +
                '>Vezi articol</a></div><p id="source"' + i + 'class="newsSource" style=" font-size: 12px; font-weight: bold; margin-left:20px; ">' + newsSource + '</p></div>');
        }
        var mySection = $('<div class="container"></div>')
        var myCol = $('<div class="card-group vgr-cards" style="margin-bottom:40px;"></div>');
        myPanel.appendTo(myCol);
        myCol.appendTo(mySection);
        mySection.appendTo('.container-fluid');
    }
}
