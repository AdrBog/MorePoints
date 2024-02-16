/**
    This add-on allows you to configure your own keyboard shortcuts.
**/

document.addEventListener("keydown", e => {
    if (e.key == "Delete"){
        e.preventDefault()
        deleteSelected()
    } else if (e.ctrlKey && e.shiftKey && e.key == "N"){
        e.preventDefault()
        createFolderDialog()
    }
})
