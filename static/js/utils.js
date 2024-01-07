function showPromptDialog(pwd, action, placeholder = "", _default = "", id = "promptDialog"){
    const dialog = document.createElement("dialog");
    dialog.id = id;
    dialog.style.width = "400px";
    dialog.innerHTML = `
        <form action="${action}" method="get">
            <input type="hidden" name="d" value="${pwd[0]}">
            <input type="hidden" name="f" value="${pwd[1]}">
            <input type="text" pattern="^[\\w\\-. ]+$" value="${_default}" placeholder="${placeholder}" name="fname" id="fname" required>
            <div>
                <input type="submit" class="button primary" value="Ok">
                <button type="button" onclick="${id}.remove()">Cancel</button>
            </div>
        </form>
    `;
    dialog.querySelector("[name='fname']").select()
    document.body.appendChild(dialog);
    dialog.showModal();
}