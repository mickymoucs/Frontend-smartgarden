import React, { useEffect, useState } from 'react'
import { getGarden } from '../services/garden'
import Card from '../components/Card'
import '../css/Home.css'


const Home=()=> {
    const [gardenInfo, setGardenInfo] = useState(// const data for test
    {
        moist_value : 90,
        moist_default: 58,
        sprinkle_1 : {
            is_auto: true,
            is_activate: false
        },
        sprinkle_2: {
            is_auto: true,
            is_activate: false
        },
        buzzer: false,
        sunroof: true
    }
     
    )
    
    useEffect(() => {
        setInterval(() => {
            getGarden().then(data => {
                setGardenInfo(data)
                console.log(data)
            })
            //console.log(gardenInfo)
        },1000)
        
    }, [])
    
    
    return (
        <div className='background'>
            <div className="header">
            <h1>🌱 My Little Garden</h1></div>
            <Card moist_value={gardenInfo.moist_value}
                moist_default={gardenInfo.moist_default} 
                is_auto1={gardenInfo.sprinkle_1.is_auto} 
                is_activate1={gardenInfo.sprinkle_1.is_activate} 
                is_auto2={gardenInfo.sprinkle_2.is_auto} 
                is_activate2={gardenInfo.sprinkle_2.is_activate} 
                buzzer={gardenInfo.buzzer}
                sunroof={gardenInfo.sunroof}/>
            
        </div>
        
    )
}
export default Home