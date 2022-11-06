import "./styles.css";

const HeaderMenu = ({ currentPath, setCurrentPath }) => {
    const activeBtn = !!(currentPath === 'analytics');
    return (
        <div className="HeaderMenu">
            <div className="HeaderMenu__list-container">
                <div className="HeaderMenu__active-requests">
                    <img src='/crest.png' alt='crest' />
                    <button
                        className={`HeaderMenu__activebtn ${!activeBtn && 'HeaderMenu__active'}`}
                        onClick={() => setCurrentPath('active')}
                    >
                        Активные заявки
                    </button>
                </div>
                <div className="HeaderMenu__other">
                    <button
                        className={`HeaderMenu__analyticsbtn ${activeBtn && 'HeaderMenu__active'}`}
                        onClick={() => setCurrentPath('analytics')}
                    >
                        Аналитика
                    </button>
                </div>
            </div>
        </div>
    )
}

export default HeaderMenu