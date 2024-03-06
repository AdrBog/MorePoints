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
async function readFile(point, path)
{
    const data = await fetch(`/open/${point}?path=${path}&filename=${filename}`)
    return await data.text()
}

/**
 * Creates an empty file on the point
 * @param {string} point 
 * @param {string} path 
 * @param {string} filename 
 */
async function createFile(point, path, filename)
{
    const data = await createFileNoReview(point, path, filename)
    reviewResponse(await data.json())
}

/**
 * Creates an empty file on the point without review
 * @param {string} point 
 * @param {string} path 
 * @param {string} filename 
 */
async function createFileNoReview(point, path, filename)
{
    return await fetch(`/create_file/${point}`, {
        method: 'POST',
        body: JSON.stringify({
            "path": path,
            "filename": filename
        }),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    })
}

/**
 * Edits an existing file, creates it in case it does not exist
 * @param {string} point 
 * @param {string} path 
 * @param {string} filename 
 * @param {string} content 
 */
async function editFile(point, path, filename, content)
{
    const data = await editFileNoReview(point, path, filename, content)
    reviewResponse(await data.json())
}

/**
 * Edits an existing file, creates it in case it does not exist without review
 * @param {string} point 
 * @param {string} path 
 * @param {string} filename 
 * @param {string} content 
 */
async function editFileNoReview(point, path, filename, content)
{
    return await fetch(`/create_file/${point}`, {
        method: 'POST',
        body: JSON.stringify({
            "path": path,
            "filename": filename,
            "content": content,
            "edit": "1"
        }),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    })
}

/**
 * Create a directory on the point
 * @param {string} point 
 * @param {string} path 
 * @param {string} foldername 
 */
async function createFolder(point, path, foldername)
{
    const data = await createFolderNoReview(point, path, foldername)
    reviewResponse(await data.json())
}

/**
 * Create a directory on the point without review
 * @param {string} point 
 * @param {string} path 
 * @param {string} foldername 
 */
async function createFolderNoReview(point, path, foldername)
{
    return fetch(`/create_folder/${point}`, {
        method: 'POST',
        body: JSON.stringify({
            "path": path,
            "filename": foldername
        }),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    })
}

/**
 * Removes a file or directory from the point
 * @param {string} point 
 * @param {string} path 
 */
async function deleteFile(point, path, filename)
{
    data = await deleteFileNoReview(point, path, filename)
    reviewResponse(await data.json())
}

/**
 * Removes a file or directory from the point without review
 * @param {string} point 
 * @param {string} path 
 */
async function deleteFileNoReview(point, path, filename)
{
    return await fetch(`/delete/${point}`, {
        method: 'POST',
        body: JSON.stringify({
            "path": path,
            "filename": filename
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
async function renameFile(point, path, filename, newName)
{
    const data = await renameFileNoReview(point, path, filename, newName)
    reviewResponse(await data.json())
}

/**
 * Rename a file or directory from the point without response
 * @param {string} point 
 * @param {string} path 
 * @param {string} filename 
 * @param {string} newName 
 */
async function renameFileNoReview(point, path, filename, newName)
{
    return await fetch(`/rename/${point}`, {
        method: 'POST',
        body: JSON.stringify({
            "path": path,
            "filename": filename,
            "new_name": newName
        }),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    })
}


/**
 * Move a file or directory
 * @param {string} point 
 * @param {string} path 
 * @param {string} filename 
 * @param {string} newPath
 */
async function moveFile(point, path, filename, newPath)
{
    const data = await moveFileNoReview(point, path, filename, newPath)
    reviewResponse(await data.json())
}


/**
 * Move a file or directory without response
 * @param {string} point 
 * @param {string} path 
 * @param {string} filename 
 * @param {string} newPath
 */
async function moveFileNoReview(point, path, filename, newPath)
{
    return await fetch(`/rename/${point}`, {
        method: 'POST',
        body: JSON.stringify({
            "path": path,
            "filename": filename,
            "new_path": newPath
        }),
        headers: {"Content-type": "application/json; charset=UTF-8"}
    })
}
