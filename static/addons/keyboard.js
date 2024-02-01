/**
    This add-on allows you to configure your own keyboard shortcuts.
**/

document.addEventListener("keydown", e => {
    switch (e.target.tagName.toLowerCase()) {
        case 'input':
            break;
        case 'textarea':
            break;
        default:
    }
})
