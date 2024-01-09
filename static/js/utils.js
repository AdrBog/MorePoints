/**
 * Utilities file for application development
 */

const VALID_FILENAME = /^(?!\s)[a-zA-Z0-9_\. ]{1,50}(?<!\s)$/g

/**
 * Executes a function depending on the status of the response returned by the flask application.
 * @param {Object} json 
 */
function reviewResponse(json){
    switch (json['status']) {
        case "Error":
            popMessage("Error", json['output'], "error")
            break;
        case "Info":
            popMessage("Info", json['output'], "info")
            break;
        case "Ok":
            location.reload()
            break;
    }
}

/**
 * Displays a pop-up dialog on the page.
 * @param {string} title 
 * @param {string} message 
 * @param {string} _class 
 */
function popMessage(title, message, _class){
    const dialog = document.createElement("dialog")
    dialog.classList.add(_class)
    dialog.style.width = "400px"
    dialog.innerHTML = `
    <p>
        <h1>${title}</h1>
        ${message}
    </p>
    <button onclick="this.parentElement.remove()">Ok</button>
    `
    document.body.append(dialog)
    dialog.showModal()
}

/**
 * Checks if a string matches a regular expression
 * @param {regexp} regex 
 * @param {string} string 
 * @returns 
 */
function match(regex, string){
    regex.lastIndex = 0;
    return regex.test(string);
}

/**
 * A prompt to ensure that the user enters a valid filename
 * @param {string} message 
 * @param {string} _default 
 * @returns 
 */
function filenamePrompt(message, _default){
    const filename = prompt(message, _default);
    if (filename === null) {
        return
    } else if (match(VALID_FILENAME, filename)){
        return filename
    } else{
        alert("Invalid filename")
        return filenamePrompt(message, filename)
    }
}