/**
 * This file contains functions for interacting with the flask application
 * Depends on utils.js
 */

/**
 * Returns the contents of a point file
 * @param {string} point 
 * @param {string} path 
 * @param {string} filename 
 * @returns 
 */
async function readFile(point, path){
    const data = await fetch(`/open/${point}?path=${path}&filename=${filename}`)
    return await data.text() 
}

/**
 * Creates an empty file on the point
 * @param {string} point 
 * @param {string} path 
 * @param {string} filename 
 */
async function createFile(point, path, filename){
    const data = await fetch(`/create_file/${point}`, {
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
 * @param {string} point 
 * @param {string} path 
 * @param {string} filename 
 * @param {string} content 
 */
async function editFile(point, path, filename, content){
    const data = await fetch(`/create_file/${point}`, {
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
 * Create a directory on the point
 * @param {string} point 
 * @param {string} path 
 * @param {string} foldername 
 */
async function createFolder(point, path, foldername){
    const data = await fetch(`/create_folder/${point}`, {
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
 * Removes a file or directory from the point
 * @param {string} point 
 * @param {string} path 
 */
async function deleteFile(point, path){
    data = await deleteFileNoReview(point, path)
    reviewResponse(await data.json())
}

/**
 * Removes a file or directory from the point without review
 * @param {string} point 
 * @param {string} path 
 */
async function deleteFileNoReview(point, path){
    return await fetch(`/delete/${point}`, {
        method: 'POST',
        body: JSON.stringify({
            "path": path
        }),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    })
}

/**
 * Rename a file or directory from the point
 * @param {string} point 
 * @param {string} path 
 * @param {string} filename 
 * @param {string} newName 
 */
async function renameFile(point, path, filename, newName){
    const data = await fetch(`/rename/${point}`, {
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
