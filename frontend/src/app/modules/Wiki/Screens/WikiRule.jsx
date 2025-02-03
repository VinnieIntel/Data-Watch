import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { IoCaretBack } from "react-icons/io5";
import styled from 'styled-components';
import { Button } from '@mui/material';
import COLORS from '../../../platform/Style/Colors';


const OuterDiv = styled.div`
    display: flex;
    flex-direction:column;
    width: calc(100% - 150px);
    padding: 1rem;
`;

const HeaderDiv = styled.div`
    display: flex;
    flex-direction:row;
    align-items: center;
`;
const StyledButton = styled(Button)`
    && {
        color: ${COLORS.white};
        &:hover {
            color: ${COLORS.lightGreen};
        }
    }
    `;

const WikiRule = () => {
    const { ruleId } = useParams(); // Dynamic parameter from the URL
    const navigate = useNavigate(); 
    const [ruleContent, setRuleContent] = useState(null); // Store the fetched rule content
    const [error, setError] = useState(null); // Store errors if any

    useEffect(() => {
        // Fetch the rule content from the backend
        const fetchRule = async () => {
            try {
                const response = await fetch(`http://localhost:5000/api/rules/${ruleId}`);
                if (!response.ok) {
                    throw new Error(`Error: ${response.statusText}`);
                }
                const data = await response.json();
                setRuleContent(data.content);
            } catch (err) {
                setError(err.message);
            }
        };

        fetchRule();
    }, [ruleId]);

    const handleBackClick = () => {
        navigate('/wiki'); 
    };


    return (
        <OuterDiv>
            <HeaderDiv>
                <StyledButton onClick={handleBackClick}><IoCaretBack size={40} /></StyledButton>
                
                <h1>Wiki Page</h1>
            </HeaderDiv>
            <h2>Rule: {ruleId}</h2>
            {error ? (
                <p style={{ color: 'red' }}>{error}</p>
            ) : ruleContent ? (
                <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
                    {ruleContent}
                </pre>
            ) : (
                <p>Loading...</p>
            )}
        </OuterDiv>
    );
};

export default WikiRule;
