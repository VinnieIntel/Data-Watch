import COLORS from '../Style/Colors';
import FONTWEIGHT from '../Style/FontWeight';

export default class NavLinkStylesUtil {
    static activeStyle = ({ isActive }) => ({
        color: isActive ? COLORS.red : COLORS.black,
    });

    static activeStyleWithFontWeight = ({ isActive }) => ({
        color: isActive ? COLORS.lightGreen : COLORS.lightBlue,
        fontWeight: isActive ? FONTWEIGHT.SEMI_BOLD : FONTWEIGHT.REGULAR,
    });
}