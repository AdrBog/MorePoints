/**
 * This file contains functions for interacting with the flask application
 * Depends on utils.js
 */

/**
 * Returns the contents of a site file
 * @param {string} site 
 * @param {string} path 
 * @returns 
 */
async function readFile(site, path){
    const data = await fetch(`/open/${site}?path=${path}`)
    return await data.text() 
}

/**
 * Creates an empty file on the site
 * @param {string} site 
 * @param {string} path 
 * @param {string} filename 
 */
async function createFile(site, path, filename){
    const data = await fetch(`/create_file/${site}`, {
        method: 'POST',
        body: JSON.stringify({
            "path": path,
            "filename": filename
        }),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    })
    reviewResponse(await data.json())
}

/**
 * Edits an existing file, creates it in case it does not exist
 * @param {string} site 
 * @param {string} path 
 * @param {string} filename 
 * @param {string} content 
 */
async function editFile(site, path, filename, content){
    const data = await fetch(`/create_file/${site}`, {
        method: 'POST',
        body: JSON.stringify({
            "path": path,
            "filename": filename,
            "content": content,
            "edit": "1"
        }),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    })
    reviewResponse(await data.json())
}

/**
 * Create a directory on the site
 * @param {string} site 
 * @param {string} path 
 * @param {string} foldername 
 */
async function createFolder(site, path, foldername){
    const data = await fetch(`/create_folder/${site}`, {
        method: 'POST',
        body: JSON.stringify({
            "path": path,
            "filename": foldername
        }),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    })
    reviewResponse(await data.json())
}

/**
 * Removes a file or directory from the site
 * @param {string} site 
 * @param {string} path 
 */
async function deleteFile(site, path){
    const data = await fetch(`/delete/${site}`, {
        method: 'POST',
        body: JSON.stringify({
            "path": path
        }),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    })
    reviewResponse(await data.json())
}

/**
 * Rename a file or directory from the site
 * @param {string} site 
 * @param {string} path 
 * @param {string} filename 
 * @param {string} newName 
 */
async function renameFile(site, path, filename, newName){
    const data = await fetch(`/rename/${site}`, {
        method: 'POST',
        body: JSON.stringify({
            "path": path,
            "filename": filename,
            "new_name": newName
        }),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    })
    reviewResponse(await data.json())
}