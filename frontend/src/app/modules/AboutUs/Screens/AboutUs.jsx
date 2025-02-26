import styled from "styled-components";

const AboutContainer = styled.div`
  padding: 40px;
  max-width: 800px;
  margin: auto;
  text-align: center;
`;

const Title = styled.h1`
  font-size: 28px;
  margin-bottom: 20px;
`;

const Description = styled.p`
  font-size: 16px;
  line-height: 1.6;
`;
const Footer = styled.div`
  position: absolute;
  bottom: 2rem;
  right: 3rem;
  font-size: 1.1rem;
  color: #a0aec0;
  text-align: right;
`;

const About = () => {
  return (
    <AboutContainer>
      <Title>About Data Watch's Development</Title>
      <Description>
        Data Watch is a monitoring system that helps track and analyze tool status in real-time.
        This project integrates Flask backend, React frontend, and scheduled automation scripts
        for data processing.
      </Description>
      <Footer>
        Developed by <b>Ong, Soon Thiam</b> & <b>Tiang, Vinnie Wen Ying</b> from PGAT Test MAPS.
      <br></br>
        --- Deployed on 20 February 2025 in PGAT. ---
      </Footer>
    </AboutContainer>
  );
};

export default About;
