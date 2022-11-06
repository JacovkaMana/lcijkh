import HeaderMenu from "../HeaderMenu/HeaderMenu";
import HeaderSearch from "../HeaderSearch/HeaderSearch";
import "./styles.css";

const HeaderBlock = ({ currentPath, setCurrentPath }) => {
    return (
        <>
            <HeaderMenu
                currentPath={currentPath}
                setCurrentPath={setCurrentPath}
            />
            <HeaderSearch />
        </>
    )
}

export default HeaderBlock