import localforage from "localforage"



export default async function getCachedBlobUrl(blobPath,cacheName){ 
  // Cache blob when connected to internet
  let blobUrl = await fetch(blobPath)
  .then(e=>{ return e.blob() })
  .then(blob=>{
    console.log('Caching ' + cacheName + ' blob')
    localforage.setItem(cacheName, blob)
    return blobPath
  })
  .catch(()=>{
    // Load blob from cache if not connected to internet
    return localforage.getItem(cacheName).then(blob=>{
      console.log('Loading ' + cacheName + ' blob from cache')
      return URL.createObjectURL(blob)
    })
  })

  return blobUrl
}