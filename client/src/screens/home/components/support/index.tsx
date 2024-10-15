import logo from '../../../../assets/logo_white_1.svg'
import tgImg from '../../../../assets/tg.svg'
import { getEnv } from '../../../../utils'

const Support = () => {
    return (
        <section className="support" id="support">
            <div className="container support__container">
                <img className="support__logo" src={logo} alt="logo" />
                <h3 className="support__title">
                    Answering your questions 24/7
                </h3>
                <div className="support__text">
                    Send message to our support!
                </div>
                <a className="support__btn" href={`${getEnv(process.env.REACT_APP_TG_SUPPORT_CHAT, 'REACT_APP_TG_SUPPORT_CHAT')}`}>
                    <img src={tgImg} alt="tg" />
                    Open chat
                </a>
            </div>
        </section>
    )
}

export default Support