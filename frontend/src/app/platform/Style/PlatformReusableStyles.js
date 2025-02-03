import COLORS from './Colors';
import FONTWEIGHT from './FontWeight';

export default class PlatformReusableStyles {
    static PrimaryButtonStyles = {
        backgroundColor: COLORS.royalBlue,
        color: COLORS.white,
        fontWeight: FONTWEIGHT.SEMI_BOLD,
        padding: '0.5rem 1rem',
    };

    static SecondaryButtonStyles = {
        color: COLORS.royalBlue,
        fontWeight: FONTWEIGHT.SEMI_BOLD,
        padding: '0.5rem 1rem',
    };

    static OutlineButtonStyles = {
        color: COLORS.darkBlue,
        border: `1px solid ${COLORS.darkBlue}`,
        fontWeight: FONTWEIGHT.SEMI_BOLD,
        padding: '0.5rem 1rem',
    };

    static BlackOutlineButtonStyles = {
        color: COLORS.black,
        border: `1px solid ${COLORS.black}`,
        fontWeight: FONTWEIGHT.SEMI_BOLD,
        padding: '0.5rem 1rem',
    };

    static GreenFilledButton = {
        backgroundColor: COLORS.lightGreen,
        border: `1px solid ${COLORS.lightGreen}`,
        fontWeight: FONTWEIGHT.SEMI_BOLD,
        color: COLORS.black,
        padding: '0.5rem 1rem',
    };

    static GreenEmptyButton = {
        fontWeight: FONTWEIGHT.SEMI_BOLD,
        color: COLORS.lightGreen,
        padding: '0.5rem 1rem',
    };
}