import axios from "axios"

export async function getGarden() {
    const res = await axios.get("http://group8.exceed19.online/garden/all")
    return res.data 
}

export async function postGarden(json) {
    console.log("Data",json)
    const res = await axios.post("http://group8.exceed19.online/garden/update", json)
    return res.data
}
