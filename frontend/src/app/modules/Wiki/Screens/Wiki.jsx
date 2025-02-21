import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { LuDownload } from "react-icons/lu";
import { Button } from '@mui/material';
import PlatformReusableStyles from '../../../platform/Style/PlatformReusableStyles';
import styled from 'styled-components';
import COLORS from '../../../platform/Style/Colors';
import FONTSIZE from '../../../platform/Style/FontSize';
import { assets } from '../../../platform/assets/assets';

const OuterDiv = styled.div`
    padding: 10px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
`;
const UpperDiv = styled.div`
    display: flex;
    flex-direction: column;
    align-items: start;
    border-bottom: 5px solid ${COLORS.lightGrey};
    padding: 10px;
`
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
    border: 1px solid ${COLORS.lightGreen};
    padding: 10px;
    border-radius: 15px;
`;

const GreenWords = styled.p`
    color: ${COLORS.lightGreen};
    font-size: ${FONTSIZE.small};
    margin-left: 10px;
`;

const StyledButton = styled(Button)`
    && {
        color: ${COLORS.lightGreen};
        &:hover {
            color: ${COLORS.white};
        }
    }
    `;

const StyledImage = styled.img`
    // margin-right: 20px;
    display: flex;
    width : 500px;
`;

const StyledImage2 = styled.img`
    margin-right: 20px;
    display: flex;
    width : 300px;
`;

const ImageDiv = styled.div`
    display: flex;
    flex-direction: row;
    align-items: center;
    border: 1px solid ${COLORS.lightGrey};
    padding: 10px;
`;

const Wiki = () => {
    const { ruleId } = useParams(); // Dynamic parameter from the URL
    const [rules, setRules] = useState([]); // Store the list of rules
    const [ruleContent, setRuleContent] = useState(null); // Store the fetched rule content
    const [error, setError] = useState(null); // Store errors if any

    useEffect(() => {
        // Fetch the list of rules from the backend
        const fetchRules = async () => {
            try {
                const response = await fetch(`${import.meta.env.VITE_API_URL}/api/rules`);
                if (!response.ok) {
                    throw new Error(`Error: ${response.statusText}`);
                }
                const data = await response.json();
                setRules(data.rules); // Assuming the API returns { rules: ["rule1.txt", "rule2.txt"] }
            } catch (err) {
                setError(err.message);
            }
        };

        fetchRules();
    }, []);

    useEffect(() => {
        // Fetch the rule content if a ruleId is provided
        const fetchRule = async () => {
            if (ruleId) {
                try {
                    const response = await fetch(`${import.meta.env.VITE_API_URL}/api/rules/${ruleId}`);
                    if (!response.ok) {
                        throw new Error(`Error: ${response.statusText}`);
                    }
                    const data = await response.json();
                    setRuleContent(data.content); // Assuming the API returns { content: "Rule content here..." }
                } catch (err) {
                    setError(err.message);
                }
            }
        };

        fetchRule();
    }, [ruleId]);

    return (
        <div>
            <h1>Wiki Page</h1>

            {/* Display list of available rules */}
            <OuterDiv>
            <UpperDiv>
                <h2>Introduction:</h2>
                <ImageDiv>
                <StyledImage src={assets.chip}></StyledImage>
                <p></p>
                {/* <StyledImage2 src={assets.tool}></StyledImage2> */}
                </ImageDiv>
                <p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
                    Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, 
                    when an unknown printer took a galley of type and scrambled it to make a type specimen book. 
                    It has survived not only five centuries, but also the leap into electronic typesetting, 
                    remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset 
                    sheets containing Lorem Ipsum passages, and more recently with desktop publishing software 
                    like Aldus PageMaker including versions of Lorem Ipsum.</p>
                    <p>
                    Netus massa imperdiet primis habitant elementum natoque feugiat; sodales montes. Mi vitae tempus 
                    efficitur posuere tristique primis libero euismod. Faucibus curae nam, commodo at class primis dictum. 
                    Consequat hendrerit etiam posuere nisl nascetur risus malesuada vulputate nascetur? Aptent phasellus 
                    malesuada tortor conubia litora hendrerit. Litora facilisi nec mi mollis; mus nisi aenean erat efficitur. 
                    Lacus condimentum luctus eu purus lacus? Proin ex id nam platea cubilia potenti justo. Vel volutpat 
                    quisque semper class eu sodales auctor.</p>
                    <p></p>
                    </UpperDiv>
                    <UpperDiv>
                <h2>Available Rules:</h2>
                {error ? (
                    <p style={{ color: 'red' }}>{error}</p>
                ) : rules.length > 0 ? (
                    <ul>
                        {rules.map((rule) => (
                            <li key={rule}>
                                <Link to={`/Wiki/${rule}`}>{rule}</Link>
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>Loading rules...</p>
                )}
            </UpperDiv>
            
            {/* Display selected rule content */}
            {ruleId && (
                <div>
                    <h2>Rule: {ruleId}</h2>
                    {error ? (
                        <p style={{ color: 'red' }}>{error}</p>
                    ) : ruleContent ? (
                        <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
                            {ruleContent}
                        </pre>
                    ) : (
                        <p>Loading rule content...</p>
                    )}
                </div>
            )}

            {/* Download RuleCreation.py file from backend data */}
            <DownloadDiv>
                <h2>Rule Creation:</h2>
                <p>Lorem ipsum odor amet, consectetuer adipiscing elit. Nulla cursus felis morbi volutpat quisque. 
                    Euismod sapien facilisi conubia tempus himenaeos. Litora magnis rhoncus dolor litora mus velit 
                    elementum facilisi porta. Rutrum fusce mi lobortis lorem in class sapien lacus taciti. Mauris 
                    commodo molestie consectetur magna diam amet maecenas mollis finibus. Sit leo interdum tincidunt 
                    amet adipiscing nec. Enim luctus mus posuere diam, amet imperdiet.
                    </p>
                    {/* <p>
                    At luctus auctor platea egestas id ultrices erat mi. Vestibulum penatibus ad efficitur consectetur 
                    cras faucibus velit quisque. Tortor aliquam quisque morbi vestibulum nunc. Lobortis dis ridiculus 
                    mauris vel primis ligula condimentum ex turpis. Enim vestibulum integer diam et interdum fusce erat 
                    morbi. Consectetur auctor mattis lacus vehicula ex placerat commodo luctus. Nisl per conubia morbi sit 
                    velit. Erat aliquam nam elit id cursus augue.
                    </p>
                    <p>
                    Dictumst hendrerit sapien platea dolor molestie sit fringilla dignissim magna. Mus dis euismod 
                    praesent elit elit faucibus nulla aenean. Venenatis tortor lacinia dis inceptos et eu quisque. 
                    Quam commodo tellus senectus vitae eros torquent semper leo. Gravida facilisis cursus id nulla 
                    donec. Adipiscing vehicula integer quis viverra finibus aliquam. Suspendisse eros augue nisi 
                    ridiculus senectus odio neque tempus. Quam eros augue suscipit ipsum scelerisque. Vivamus pretium 
                    nunc eget fusce curae sociosqu amet justo.
                    </p>
                    <p>
                    Feugiat vestibulum quisque quisque egestas imperdiet cursus non iaculis. Inceptos curae dignissim 
                    ornare facilisi nascetur tempus. Porta ut turpis adipiscing facilisis diam. Phasellus ex inceptos 
                    efficitur consectetur lobortis inceptos gravida rhoncus. Proin et fringilla sociosqu arcu vehicula 
                    senectus integer nisi. Molestie aptent primis; aliquet aenean habitant enim. Habitant neque porttitor 
                    lacinia ultrices dolor finibus eu nunc.
                    </p>
                    <p>
                    Netus massa imperdiet primis habitant elementum natoque feugiat; sodales montes. Mi vitae tempus 
                    efficitur posuere tristique primis libero euismod. Faucibus curae nam, commodo at class primis dictum. 
                    Consequat hendrerit etiam posuere nisl nascetur risus malesuada vulputate nascetur? Aptent phasellus 
                    malesuada tortor conubia litora hendrerit. Litora facilisi nec mi mollis; mus nisi aenean erat efficitur. 
                    Lacus condimentum luctus eu purus lacus? Proin ex id nam platea cubilia potenti justo. Vel volutpat 
                    quisque semper class eu sodales auctor.</p>
                    <p>
                    Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical 
                    Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor 
                    at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, 
                    from a Lorem Ipsum passage, and going through the cites of the word in classical literature, 
                    discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de 
                    Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book 
                    is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem 
                    Ipsum, "Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.
                    </p> */}
                    <p></p>
                <DownloadInnerDiv>
                    <GreenWords>Script Template</GreenWords>
            
                        <a
                            href="http://localhost:5000/api/download/rule-python"
                            download="Rule-Creation-Template"
                            target="_blank"
                            rel="noreferrer"
                            
                        >
                            <StyledButton><LuDownload size={25} /></StyledButton>
                        </a>
                    </DownloadInnerDiv>
                </DownloadDiv>
            </OuterDiv>

            {/* Download RuleCreation.py from frontend public
            <a
                href="/assets/RuleCreation.py"
                download="RuleCreation.py"
            >
                <button>Download Rule Creation Script Template</button>
            </a> */}

        </div>
    );
};

export default Wiki;
