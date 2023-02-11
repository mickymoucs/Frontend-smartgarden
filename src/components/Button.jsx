import React from 'react'
import '../css/Button.css'

const Button = ({ name, type, onClick }) => {
    return (
        <button className="button" type={type} onClick={onClick}>
            {name}
        </button>
    )
}

export default Button