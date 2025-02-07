import React, { useEffect, useState } from 'react';
import axios from 'axios';
import styled from 'styled-components';
import COLORS from '../../../platform/Style/Colors';

// Outer container for the page
const Container = styled.div`
  padding: 24px;
  border: 5px solid ${COLORS.darkGrey}; 
`;

// Title styling
const Title = styled.h1`
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 16px;
`;

// Scrollable container for the log lines
const LogContainer = styled.div`
  background-color: ${COLORS.logDarkBlue};
  color: #fff;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  max-height: 400px;
  overflow-y: auto;
`;

// Individual log line styling; change background color based on the log level.
const LogLine = styled.pre`
  background-color: ${(props) =>
    props.level === 'ERROR'
      ? '#dc2626'   /* Red for errors */
      : props.level === 'WARNING'
      ? '#f59e0b'   /* Amber for warnings */
      : '#374151'}; /* Dark gray for other logs */
  margin-bottom: 8px;
  padding: 8px;
  border-radius: 4px;
  white-space: pre-wrap;
  word-wrap: break-word;
`;

const Error = () => {

    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [fetchError, setFetchError] = useState(null);

    // Function to fetch logs from the backend API.
    const fetchLogs = async () => {
        try {
        const response = await axios.get('http://localhost:5000/api/errors');
        setLogs(response.data);
        setLoading(false);
        } catch (err) {
        setFetchError('Unable to fetch logs. Please check the backend.');
        setLoading(false);
        }
    };

    // Fetch logs when the component mounts and then refresh every 5 seconds.
    useEffect(() => {
        fetchLogs();
        const interval = setInterval(fetchLogs, 60000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div>
        <h1>Error Logs</h1>
        <Container>
          
          {loading ? (
            <p>Loading logs...</p>
          ) : fetchError ? (
            <p style={{ color: 'red' }}>{fetchError}</p>
          ) : (
            <LogContainer>
              {logs.length === 0 ? (
                <p>No error logs found.</p>
              ) : (
                logs.map((log, index) => {
                  // Determine log level from the log content:
                  let level = 'NORMAL';
                  if (log.includes('ERROR')) level = 'ERROR';
                  else if (log.includes('WARNING')) level = 'WARNING';
                  return (
                    <LogLine key={index} level={level}>
                      {log}
                    </LogLine>
                  );
                })
              )}
            </LogContainer>
          )}
        </Container>
        </div>
      );
};

export default Error;