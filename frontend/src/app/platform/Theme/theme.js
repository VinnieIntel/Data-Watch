import { createTheme } from '@mui/material/styles';
import COLORS from '../Style/Colors';

const theme = createTheme({
    components: {
        MuiCheckbox: {
            styleOverrides: {
                root: {
                    stroke: COLORS.lightGrey,
                    color: COLORS.lightGrey,
                    strokeWidth: 0,
                    '&.Mui-checked': {
                        color: COLORS.red,
                    },
                },
            },
        },
        MuiButton: {
            styleOverrides: {
                root: {
                    borderRadius: 5,
                    '&.Mui-disabled': {
                        background: COLORS.white,
                        color: COLORS.black,
                    },
                    padding: '0.8rem',
                },
            },
        },
        MuiRadio: {
            styleOverrides: {
                root: {
                    color: COLORS.lightGrey,
                    '&.Mui-checked': {
                        color: COLORS.red,
                    },
                },
            },
        },
    },
});

export default theme;