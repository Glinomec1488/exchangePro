import { links } from "./config/links"
import logoWhite from '../../assets/logo_white_1.svg'
import { Link } from "react-router-dom"
import { useState } from "react"

const Header = () => {
    const [isActiveBurder, setIsActiveBurger] = useState(false)

    return (
        <header className="header animate__animated animate__fadeInDown">
            <div className="container header__container">
                <div className="header__body">
                    <Link className="header__logo header__logo-hide" to='/'>
                        <img src={logoWhite} alt="logo" />
                    </Link>
                    <div className="header__hide">
                        <Link className="header__logo" to='/'>
                            <img src={logoWhite} alt="logo" />
                        </Link>
                        <nav className="header__nav">
                            <ul className="header__list">
                                {
                                    links.map(link => (
                                        <li key={link.name} className="header__item">
                                            <a className="header__link" href={`${link.href}`}>{link.name}</a>
                                        </li>
                                    ))
                                }
                            </ul>
                        </nav>
                        <div className="header__wrapper">
                            {/* <div className="header__lang">
                                <div className="header__lang-lang">
                                    <a className="header__lang-wrapper" href="">
                                        <img src={uaImg} alt="ua" />
                                        <div className="header__lang-text">
                                            Eng
                                        </div>
                                    </a>
                                    <a className="header__lang-wrapper header__lang-dropdown" href="#">
                                        <img src={ruImg} alt="ru" />
                                        <div className="header__lang-text">
                                            Ru
                                        </div>
                                    </a>
                                </div>
                                <img className="header__lang-arrow" src={arrowImg} alt="arrow" />
                            </div> */}
                            <a className="header__btn" href="#exchange">
                                Exchange
                            </a>
                        </div>
                    </div>
                    <div onClick={() => setIsActiveBurger(prev => !prev)} className="header__burger">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
                <div
                    className={
                        isActiveBurder
                            ? "header__burger-content_active"
                            : "header__burger-content"
                    }
                >
                    <nav className="header__nav">
                        <ul className="header__list">
                            {
                                links.map(link => (
                                    <li key={link.name} className="header__item">
                                        <a className="header__link" href={`${link.href}`}>{link.name}</a>
                                    </li>
                                ))
                            }
                        </ul>
                        <a className="header__btn" href="#exchange">
                            Exchange
                        </a>
                    </nav>
                    <div className="header__wrapper">
                        {/* <div className="header__lang">
                            <div className="header__lang-lang">
                                <a className="header__lang-wrapper" href="">
                                    <img src="/images/ua.svg" alt="ua" />
                                    <div className="header__lang-text">
                                        Eng
                                    </div>
                                </a>
                                <a className="header__lang-wrapper header__lang-dropdown" href="#">
                                    <img src="/images/ru.svg" alt="ru" />
                                    <div className="header__lang-text">
                                        Ru
                                    </div>
                                </a>
                            </div>
                            <img className="header__lang-arrow" src="/images/arrow.svg" alt="arrow" />
                        </div> */}
                        {/* <a className="header__btn" href="#exchange">
                            Exchange
                        </a> */}
                    </div>
                </div>
            </div>
        </header>
    )
}

export default Header