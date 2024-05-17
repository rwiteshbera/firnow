import React, { useState, useEffect } from 'react';
//import axios from 'axios';
import { FaPlus } from 'react-icons/fa';

import { sampleFIRDetail, sampleCaseStatusOptions, samplePoliceStations } from './sampledata';


import "./firdetails.css";

const FIRDetails = ({ firId }) => {

    /*
       //needed if axios used
      const [firDetail, setFIRDetail] = useState(null);
      const [caseStatusOptions, setCaseStatusOptions] = useState([]);
      const [policeStations, setPoliceStations] = useState([]);
    */
    const [showNotePanel, setShowNotePanel] = useState(false);
    const [noteText, setNoteText] = useState('');
    const [selectedStatus, setSelectedStatus] = useState('');
    const [selectedPoliceStation, setSelectedPoliceStation] = useState('');
    const [firDetail, setFIRDetail] = useState(sampleFIRDetail);
    const [caseStatusOptions, setCaseStatusOptions] = useState(sampleCaseStatusOptions);
    const [policeStations, setPoliceStations] = useState(samplePoliceStations);



    const handleAddNote = () => {
        setShowNotePanel(true);
    };

    // const fetchFIRDetail = async () => {
    //     try {
    //         const response = await axios.get(`/api/firs/${firId}`);
    //         setFIRDetail(response.data);
    //     } catch (error) {
    //         console.error('Error fetching FIR detail:', error);
    //     }
    // };

    // const fetchCaseStatusOptions = async () => {
    //     try {
    //         const response = await axios.get('/api/case-status-options');
    //         setCaseStatusOptions(response.data);
    //     } catch (error) {
    //         console.error('Error fetching case status options:', error);
    //     }
    // };

    // const fetchPoliceStations = async () => {
    //     try {
    //         const response = await axios.get('/api/police-stations');
    //         setPoliceStations(response.data);
    //     } catch (error) {
    //         console.error('Error fetching police stations:', error);
    //     }
    // };


    // useEffect(() => {
    //     fetchFIRDetail();
    //     fetchCaseStatusOptions();
    //     fetchPoliceStations();
    // }, [firId]); 

    // const handleSaveNote = async () => {
    //     try {
    //         // Send a request to the backend to save the note
    //         await axios.post(`/api/firs/${firId}/notes`, { note: noteText });
    //         // Refresh the FIR detail after saving the note
    //         fetchFIRDetail();
    //         // Close the note input panel
    //         setShowNotePanel(false);
    //         // Clear the note text
    //         setNoteText('');
    //     } catch (error) {
    //         console.error('Error saving note:', error);
    //     }
    // };

    // const handleUpdateCaseStatus = async () => {
    //     try {
    //         await axios.put(`/api/firs/${firId}/status`, { status: selectedStatus });
    //         // Optionally update FIR details after successful update
    //         fetchFIRDetail();
    //     } catch (error) {
    //         console.error('Error updating case status:', error);
    //     }
    // };

    // const handleAssignToPoliceStation = async () => {
    //     try {
    //         await axios.put(`/api/firs/${firId}/assign`, { policeStationId: selectedPoliceStation });
    //         // Optionally update FIR details after successful update
    //         fetchFIRDetail();
    //     } catch (error) {
    //         console.error('Error assigning to police station:', error);
    //     }
    // };

    const handleSaveNote = () => {
        const updatedFIRDetail = { ...firDetail }; 
        updatedFIRDetail.notes.push(noteText); 
        setFIRDetail(updatedFIRDetail); 
        setShowNotePanel(false); // Hiding the note input panel
        setNoteText(''); 
    };
  

    // this feature not updating status in db rn
    const handleUpdateCaseStatus = () => {
        const updatedFIRDetail = { ...firDetail }; 
        updatedFIRDetail.status = selectedStatus; 
        setFIRDetail(updatedFIRDetail); 
    };

    const handleAssignToPoliceStation = () => {
        const updatedFIRDetail = { ...firDetail }; 
        updatedFIRDetail.assignedStation = selectedPoliceStation; 
        setFIRDetail(updatedFIRDetail); 
    };


    if (!firDetail) {
        return <div className="fir-detail-container">Loading FIR detail...</div>;
    }

    return (
        <div className="fir-detail-container">
            <h3 className="ffir-detail-title">FIR Details</h3>
            <p className="fir-detail-item-container"><strong>Case Number:</strong> {firDetail.caseNumber}</p>
            <p className="fir-detail-item-container"><strong>Date:</strong> {firDetail.date}</p>
            <p className="fir-detail-item-container"><strong>Location:</strong> {firDetail.location}</p>
            <p className="fir-detail-item-container"><strong>Complainant:</strong> {firDetail.complainant}</p>
            <p className="fir-detail-item-container"><strong>Description:</strong> {firDetail.description}</p>
            <div>
                <h4>Attached Documents</h4>
                {firDetail.documents.map((document, index) => (
                    <div key={index} className="fir-detail-item">
                        <a href={document.url} target="_blank" rel="noopener noreferrer">{document.name}</a>
                    </div>
                ))}
            </div>
            <div className="fir-detail-item-container">
                <button className="add-note-btn" onClick={handleAddNote}>
                    <FaPlus /> Add Note
                </button>
            </div>
            {showNotePanel && (
                <div className="fir-detail-item-container">
                    <textarea
                        value={noteText}
                        onChange={(e) => setNoteText(e.target.value)}
                        placeholder="Enter your note..."
                    />
                    <div>
                        <button className="save-note-btn"
                            onClick={handleSaveNote}
                            disabled={!noteText.trim()}>Save</button>
                    </div>
                </div>
            )}
            {firDetail.notes.map((note, index) => (
                <div key={index} className="fir-detail-item-container">{note}</div>
            ))}

            <div className="status-container">
                <select className="select-box" value={selectedStatus} onChange={(e) => setSelectedStatus(e.target.value)}>
                    <option value="">Select Case Status</option>
                    {caseStatusOptions.map((status, index) => (
                        <option key={index} value={status}>{status}</option>
                    ))}
                </select>
                <button className="update-status-btn" onClick={handleUpdateCaseStatus}>Update Case Status</button>
            </div>
            <div className="status-container">
                <select className="select-box" value={selectedPoliceStation} onChange={(e) => setSelectedPoliceStation(e.target.value)}>
                    <option value="">Select Police Station</option>
                    {policeStations.map((station, index) => (
                        <option key={index} value={station.id}>{station.name}</option>
                    ))}
                </select>
                <button className="update-status-btn" onClick={handleAssignToPoliceStation}>Assign to Police Station</button>
            </div>
        </div>
    );
};

export default FIRDetails;
