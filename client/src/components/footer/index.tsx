import tgImg from "../../assets/tg_1.svg";
import logoSmallWhite from "../../assets/logo_small_white_1.svg";
import { getEnv } from "../../utils";
import bestchange from "../../assets/bestchange-footer.svg";
import trustPilot from "../../assets/Trust-Pilot.svg";
const Footer = () => {
  return (
    <footer className="footer">
      <div className="container footer__container">
        <div className="footer__start">
          <img
            style={{ height: "50px", width: "50px" }}
            className="footer__logo"
            src={logoSmallWhite}
            alt="logo"
          />
          <div className="footer__text">ALL RIGHTS RESERVED © 2024</div>
        </div>
        <div className="footer__mid">
          <a className="footer__link" href="">
            <img src={bestchange} className="footer__reput1" />
          </a>
          <a className="footer__link" href="">
            <img src={trustPilot} className="footer__reput2" />
          </a>
        </div>
        <div className="footer__end">
          <a
            className="footer__link"
            href={`${getEnv(
              process.env.REACT_APP_TG_SUPPORT_CHAT,
              "REACT_APP_TG_SUPPORT_CHAT"
            )}`}
          >
            <img src={tgImg} alt="tg" />
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
