import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import COLORS from '../../../platform/Style/Colors';

const OuterDiv = styled.div`
    display: flex;
    flex-direction: column;
    width: calc(100% - 150px);
    padding: 1rem;
`;

const InnerDiv = styled.div`
    overflow: auto;
    width: 100%;
    max-height: 400px;
    max-width: 100%;
    border: 5px solid ${COLORS.lightGreen}; 
    overflow-y: auto;
`;

const StyledTable = styled.table`
    width: 100%;
    border-collapse: collapse;
    border: 1px solid ${COLORS.lightGreen};
`;

const StyledTh = styled.th`
    position: sticky;
    top: 0;
    z-index: 1; 
    background-color: ${COLORS.lightGreen};
    color: black;
    white-space: nowrap;
    padding: 8px;
    text-align: center;
`;

const StyledTd = styled.td`
    white-space: nowrap;
    padding: 8px;
    border: 1px solid ${COLORS.lightGreen};
    text-align: center;
    vertical-align: middle;
`;

const StatusCell = styled(StyledTd)`
    font-weight: bold;
    color: ${props => {
        switch (props.$status) {
            case 'PROD':
                return COLORS.lightGreen;
            case 'STANDBY':
                return COLORS.yellow;
            case 'Unknown':
                return 'grey';
            case 'PM':
                return COLORS.hotPink;
            case 'BAGGED':
                return COLORS.brightGrey;
            case '-':
                return 'inherit';
            default:
                return 'red';
        }
    }};
`;

const Status = () => {
    const [columns, setColumns] = useState([]);
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(`${import.meta.env.VITE_API_URL}/api/status`);
                if (!response.ok) {
                    throw new Error(`Error: ${response.statusText}`);
                }
                const result = await response.json();
                console.log('Fetched data:', result); // Log the fetched data

                if (result.data.length > 0) {
                    setColumns(result.columns);
                    setData(result.data);
                } else {
                    setError('No data available');
                }
                setLoading(false);
            } catch (error) {
                console.error('Error fetching data:', error);
                setError(error.message);
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    return (
        <div>
        <h1>Tool Status</h1>
        <OuterDiv>
            
            {loading ? (
                <p>Loading...</p>
            ) : error ? (
                <p style={{ color: 'red' }}>{error}</p>
            ) : (
                <InnerDiv>
                    <StyledTable>
                        <thead>
                            <tr>
                                {columns.map((col, index) => (
                                    <StyledTh key={index}>{col}</StyledTh>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {data.map((row, rowIndex) => (
                                <tr key={rowIndex}>
                                    {columns.map((col, colIndex) => (
                                        col === 'STATUS' ? (
                                            <StatusCell key={colIndex} $status={row[col]}>
                                                {row[col]}
                                            </StatusCell>
                                        ) : (
                                            <StyledTd key={colIndex}>
                                                {row[col] || ''}
                                            </StyledTd>
                                        )
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </StyledTable>
                </InnerDiv>
            )}
        </OuterDiv>
        </div>
    );
};

export default Status;