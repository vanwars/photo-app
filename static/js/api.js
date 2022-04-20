let textboxId;
let targetId;
let requestBody;
let method;
let pre;
let url;
    
const sendRequest = ev => {
    console.log(ev);
    textboxId = ev.currentTarget.dataset.textbox;
    targetId = ev.currentTarget.dataset.target;
    requestBody = ev.currentTarget.dataset.request_body;
    method = ev.currentTarget.dataset.method;
    pre = document.getElementById(targetId);
    url = document.getElementById(textboxId).value;
    console.log(textboxId, targetId, method);
    console.log(url);
    if (method === 'get') {
        sendGetRequest(pre, url)
    } else if (['post', 'patch'].includes(method.toLowerCase())) {
        let elem = document.getElementById(requestBody);
        try {
            const val =  elem.innerHTML.replace(/(<([^>]+)>)/gi, "");
            let body = JSON.parse(val);
            sendPostPatchRequest(pre, url, method, body);
        } catch {
            alert('Invalid JSON: ' + val);
        }
    } else if (method === 'delete') {
        sendDeleteRequest(pre, url);
    } else {
        pre.innerHTML = 'Unrecognized method.';
    }
};

const displayStatusCode = response => {
    let elem = document.getElementById(textboxId + '-status-code');
    elem.classList.remove('active');
    elem.innerHTML = `${response.status} ${response.statusText}`;
    hljs.highlightElement(elem);
    setTimeout(() => {elem.classList.add('active')} , 0);
};

const displayResponse = (data, elem) => {
    console.log(data);
    // elem.classList.remove('active');
    elem.innerHTML = JSON.stringify(data, null, 3);
    hljs.highlightElement(elem);
    setTimeout(() => {elem.classList.add('active')} , 1);
};

const sendGetRequest = (elem, url) => {
    elem.classList.remove('active');
    fetch(url)
        .then(response => {
            displayStatusCode(response);
            return response.json()
        })
        .then(data => displayResponse(data, elem));
};

const sendPostPatchRequest = (elem, url, method, body) => {
    elem.classList.remove('active');
    fetch(url, {
            method: method.toUpperCase(),
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        })
        .then(response => {
            displayStatusCode(response);
            return response.json()
        })
        .then(data => displayResponse(data, elem));
};

const sendDeleteRequest = (elem, url) => {
    elem.classList.remove('active');
    fetch(url, { method: 'DELETE' })
        .then(response => {
            displayStatusCode(response);
            return response.json()
        })
        .then(data => displayResponse(data, elem));
};


hljs.highlightAll();