import "./styles.css";
import mglass from './../../images/loupe.png'
import cloud from './../../images/cloudy.png'

const HeaderSearch = (props) => {
    return (
        <div className="HeaderSearch">
            <div className="HeaderSearch__container">
                <div className="HeaderSearch__searchbar">
                    <form>
                        <input className="HeaderSearch__input" name="request-search" placeholder="поиск по наименованию/карте" />
                        <input className="HeaderSearch__submit" type="submit" name="request-searchbtn"></input>
                        <button><img src={mglass} alt="mglass" /></button>
                    </form>
                </div>
                <div className="HeaderSearch__weather">
                    <div className="weather__degrees">
                        +2 C°
                    </div>
                    <div className="weather__wind">
                        8 м/с
                    </div>
                    <div className="weather__icon">
                        <img src={cloud} alt="weatherimg" />
                    </div>
                </div>
            </div>
        </div>
    )
}

export default HeaderSearch