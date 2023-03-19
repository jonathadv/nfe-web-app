function onScanSuccess(decodedText, decodedResult) {
    // Handle on success condition with the decoded text or result.
    console.log(`Scan result: ${decodedText}`, decodedResult);
    html5QrcodeScanner.clear();
    
    setFormUrl()
    document.getElementById('nfe-url-input').value=decodedResult.decodedText
    document.getElementById('nfe-form-input').submit()
}

function onScanError(errorMessage) {
    // handle on error condition, with error message
    console.log("Error while reading: ", errorMessage);
}

var html5QrcodeScanner = new Html5QrcodeScanner("reader", { fps: 10, qrbox: 250 });
html5QrcodeScanner.render(onScanSuccess, onScanError);



function stopLoader(counter) {
    document.getElementById("wrapper").className = "wrapper"
    document.getElementById("loader").style = "display:none"
}

function startLoader(counter) {
    document.getElementById("wrapper").className = "blur wrapper"
    document.getElementById("loader").style = "display:block"
}

function runWithRetries(func, numOfRetries = 20) {
    console.log("Running function, ", func, "; numOfRetries=", numOfRetries)

    try {
        func()
    } catch (err) {
        console.log("Error fount in ", func, " error: ", err, "; numOfRetries=", numOfRetries)

        if (numOfRetries <= 0){
            alert("Error: " + err)
            return
        }

        setTimeout(() => {
            runWithRetries(func, --numOfRetries)
        }, 500);
    }
}


stopLoader()


function fixScanButton() {
    var scanButton = document.getElementById("reader__camera_permission_button")
    if (scanButton) {
        scanButton.textContent = "Scan"
    }
    
}

function fixReaderDiv() {
    document.getElementById("reader").style=""
    document.getElementById('reader__dashboard_section_csr').style=""
}

function styleButtons() {
    for (let item of document.getElementsByTagName("button")) {    
        if (item.className != "btn btn-outline-info") {
            item.className="btn btn-outline-info";
            item.type="button";
        }
    }
}

function forEver(){
    try {
        styleButtons()
        fixScanButton()
    } catch(e){}

    setTimeout(() => {
        forEver()
    }, 500);
}

forEver()


function setFormUrl(){    
    document.getElementById("nfe-form-input").action = document.getElementById("nfe-server-address").value;
}