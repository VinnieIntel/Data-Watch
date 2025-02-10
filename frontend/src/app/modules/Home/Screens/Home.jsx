import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import COLORS from '../../../platform/Style/Colors';
import { Link } from 'react-router-dom';
import FONTSIZE from '../../../platform/Style/FontSize';
import { Button } from '@mui/material';
import { LuDownload } from "react-icons/lu";

const OuterDiv = styled.div`
    display: flex;
    flex-direction:column;
    width: calc(100% - 150px);
    padding: 1rem;
    justify-content: space-between;
`;

const InnerDiv = styled.div`
    overflow: auto;
    width: 100%;
    max-height: 400px;
    max-width: 100%;
    border: 5px solid ${COLORS.lightGreen}; 
    overflow-y:auto;
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
    background-color:${COLORS.lightGreen};
    color: black;
    white-space: nowrap;
    padding: 8px;
    border: 1px solid #ddd;
`;

const StyledTd = styled.td`
    white-space: nowrap;
    padding: 8px;
    border: 1px solid ${COLORS.lightGreen};
`;

const DownloadDiv = styled.div`
    display: flex;
    flex-direction: column;
    align-items: start;
    // border: 1px solid ${COLORS.lightGrey};
    padding: 10px;
`;
const DownloadInnerDiv = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    border: 2px solid ${COLORS.lightGreen};
    padding: 10px;
    border-radius: 15px;
    background-color:${COLORS.lightestGreen};
`;

const GreenWords = styled.p`
    color: ${COLORS.forestGreen};
    font-size: ${FONTSIZE.small};
    margin-left: 10px;
    font-weight: bold;
`;

const StyledButton = styled(Button)`
    && {
        color: ${COLORS.forestGreen};
        &:hover {
            color: ${COLORS.white};
        }
    }
`;

const HomePage = () => {
    const [columns, setColumns] = useState([]);
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch('http://127.0.0.1:5000/api/csv')
            .then(response => response.json())
            .then(result => {
                setColumns(result.columns);
                setData(result.data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                setLoading(false);
            });
    }, []);

    return (
        <div>
            <h1>Data Watch Trigger Data</h1>
        <OuterDiv>
            
            {loading ? (
                <p>Loading...</p>
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
                                        <StyledTd key={colIndex}>
                                        {col === 'Rule' ? (
                                            <Link to={`/Wiki/${row[col]}`}>{row[col]}</Link>
                                        ) : (
                                            row[col] || ''
                                        )}
                                    </StyledTd>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </StyledTable>
                </InnerDiv>
            )}
            <p></p>
            <DownloadDiv>
                <h2>Download Full CSV file</h2>
            <DownloadInnerDiv>
                <GreenWords>Full CSV file</GreenWords>
                <a
                    href="http://localhost:5000/api/download/full-csv"
                    download="Full_CSV"
                    target="_blank"
                    rel="noreferrer"
                    
                >
                    <StyledButton><LuDownload size={25} /></StyledButton>
                </a>
            </DownloadInnerDiv>
            </DownloadDiv>
        </OuterDiv>
        </div>
    );
};

export default HomePage;





// import React, { useEffect, useState } from 'react';

// const HomePage = () => {
//     const [csvData, setCsvData] = useState([]);
//     const [error, setError] = useState(null);

//     useEffect(() => {
//         // Fetch data from Flask API
//         fetch('http://127.0.0.1:5000/api/csv')
//             .then((response) => {
//                 if (!response.ok) {
//                     throw new Error(`HTTP error! status: ${response.status}`);
//                 }
//                 return response.json();
//             })
//             .then((data) => setCsvData(data))
//             .catch((error) => setError(error.message));
//     }, []);

//     return (
//         <div>
//             <h1>CSV Data</h1>
//             {error && <p>Error: {error}</p>}
//             {csvData.length > 0 ? (
//                 <table border="1">
//                     <thead>
//                         <tr>
//                             {Object.keys(csvData[0]).map((key) => (
//                                 <th key={key}>{key}</th>
//                             ))}
//                         </tr>
//                     </thead>
//                     <tbody>
//                         {csvData.map((row, index) => (
//                             <tr key={index}>
//                                 {Object.values(row).map((value, i) => (
//                                     <td key={i}>{value}</td>
//                                 ))}
//                             </tr>
//                         ))}
//                     </tbody>
//                 </table>
//             ) : (
//                 <p>Loading...</p>
//             )}
//         </div>
//     );
// };

// export default HomePage;