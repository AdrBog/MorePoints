async function readFile(site, path){
    const data = await fetch(`/open/${site}?path=${path}`)
    return await data.text() 
}