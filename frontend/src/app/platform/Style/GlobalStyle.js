import { createGlobalStyle } from 'styled-components';

const GlobalStyle = createGlobalStyle`
  p, a, span, label {
    font-family: 'RobotO', 'Helvetica', sans-serif;
  }
  h1, h2, h3, h4, h5, h6 {
    font-family: 'Lato', 'Georgia' serif;
  }
`;

export default GlobalStyle;