import React from "react";
import Card from '../components/Status/Card.jsx';
import StatusData from "./StatusData.jsx";
import './status.css';

export default function Status(){
    
    return(
     <>
        <div className="status-container">
        {console.log(StatusData)}
        {StatusData.map(function display (val, idx, array) {
            return(
                <>
                    <Card name={val.name} status={val.status} data ={val.data}></Card>
                </>
            )
        })}
        </div>
     </>
    );
}